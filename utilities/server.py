import json
import re
import subprocess
import time
from io import BytesIO
from pathlib import Path

import numpy as np
import soundfile
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from utilities.preprocessor import clean_text
from utilities.tts_engine import KokoroAdapter

_here = Path(__file__).resolve().parent
voice_map = json.loads((_here / "voice_map.json").read_text())
voices_dir = _here.parent / "voices"

adapter = KokoroAdapter(lang_code="a", device="auto")

app = FastAPI(title="kvoicewalk TTS Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FORMAT_MIME: dict[str, str] = {
    "wav": "audio/wav",
    "flac": "audio/flac",
    "opus": "audio/opus",
    "aac": "audio/aac",
}

VALID_FORMATS: set[str] = set(FORMAT_MIME.keys())
MAX_INPUT_CHARS: int = 5000


class TTSRequest(BaseModel):
    model: str = "kokoro"
    input: str
    voice: str = "af_bella"
    response_format: str = "wav"
    speed: float = Field(default=1.0, ge=0.25, le=4.0)


def error_response(message: str, code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={"error": {"message": message, "type": "invalid_request_error", "code": code}},
    )


def sanitize_voice(voice: str) -> str:
    if not re.match(r'^[a-zA-Z0-9_-]+$', voice):
        raise ValueError(f"Invalid voice: {voice}")
    return voice


@app.middleware("http")
async def limit_body_size(request: Request, call_next):
    if request.headers.get("content-length"):
        size = int(request.headers["content-length"])
        if size > 1_000_000:
            return JSONResponse(
                status_code=413,
                content={"error": {"message": "Request too large", "type": "invalid_request_error", "code": 413}},
            )
    return await call_next(request)


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "kokoro", "object": "model", "created": int(time.time()), "owned_by": "kvoicewalk"},
        ],
    }


@app.post("/v1/audio/speech")
async def create_speech(req: TTSRequest):
    if req.model != "kokoro":
        return error_response(f"Unsupported model: {req.model}", 400)

    input_text = req.input.strip()
    if not input_text:
        return error_response("input must be non-empty", 400)

    if req.response_format == "mp3":
        return error_response(
            "mp3 not supported, use wav/flac/opus/aac",
            400,
        )

    if req.response_format not in VALID_FORMATS:
        return error_response(
            f"Unsupported response_format: {req.response_format}. "
            f"Supported: {', '.join(sorted(VALID_FORMATS))}",
            400,
        )

    try:
        voice_name = sanitize_voice(req.voice)
    except ValueError as e:
        return error_response(str(e), 400)

    pt_file = voice_map.get(voice_name, voice_name)
    pt_path = voices_dir / f"{pt_file}.pt"
    if not pt_path.exists():
        return error_response(f"Voice '{req.voice}' not found", 400)

    if len(input_text) > MAX_INPUT_CHARS:
        input_text = input_text[:MAX_INPUT_CHARS]

    cleaned = clean_text(input_text)
    sr, audio = adapter.generate(cleaned, str(pt_path), speed=req.speed)

    fmt = req.response_format
    content_type = FORMAT_MIME[fmt]

    if fmt == "aac":
        raw = (audio * 32767).astype(np.int16).tobytes()
        proc = subprocess.run(
            ["ffmpeg", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0",
             "-c:a", "aac", "-b:a", "192k", "-f", "adts", "pipe:1"],
            input=raw,
            capture_output=True,
        )
        if proc.returncode != 0:
            return error_response("Audio encoding failed", 500)
        data = proc.stdout
    else:
        buf = BytesIO()
        sf_format = "ogg" if fmt == "opus" else fmt
        soundfile.write(buf, audio, sr, format=sf_format)
        data = buf.getvalue()

    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="speech.{fmt}"'},
    )
