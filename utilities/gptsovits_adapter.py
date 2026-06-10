import logging
import threading
from io import BytesIO

import httpx
import numpy as np
import soundfile as sf

from utilities.tts_engine import TTSEngine

logger = logging.getLogger(__name__)


class GPTSoVITSUnavailable(RuntimeError):
    """GPT-SoVITS server unreachable or timed out → 503"""


class GPTSoVITSNotFound(RuntimeError):
    """Voice not found on GPT-SoVITS side → 404"""


class GPTSoVITSAPIError(RuntimeError):
    """GPT-SoVITS returned unexpected error → 502"""


class GPTSoVITSAdapter(TTSEngine):
    """
    线程安全的 GPT-SoVITS HTTP 客户端适配器。

    通过 httpx 调用 127.0.0.1:9880/tts，返回 numpy 音频数组。
    Lock 仅护 _get_client() 初始化；HTTP 请求本身不持锁（httpx.Client 是线程安全的）。

    注意：voice_map 是 server.py 中 voice_map["gpt-sovits"] 的引用共享。
    当前无人修改 voice_map，若未来增加热加载功能需注意引用一致性。
    """

    def __init__(
        self,
        voice_map: dict,
        base_url: str = "http://127.0.0.1:9880",
        timeout: int = 30,
    ):
        self.voice_map = voice_map
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.Client | None = None
        self._lock = threading.Lock()

    def generate(self, text: str, voice: str, speed: float = 1.0, **kwargs) -> tuple[int, np.ndarray]:
        # 1. 查 voice_map（读操作无需锁）
        cfg = self.voice_map.get(voice)
        if cfg is None:
            raise GPTSoVITSNotFound(f"Voice '{voice}' not found for GPT-SoVITS")

        # 2. 校验必需字段（防 KeyError → M-06）
        required = ["text_lang", "ref_audio", "prompt_text", "prompt_lang"]
        for key in required:
            if key not in cfg:
                raise GPTSoVITSAPIError(
                    f"Voice '{voice}' missing required field '{key}' in config"
                )

        # 3. 构造请求
        payload = {
            "text": text,
            "text_lang": cfg["text_lang"],
            "ref_audio_path": cfg["ref_audio"],
            "prompt_text": cfg["prompt_text"],
            "prompt_lang": cfg["prompt_lang"],
            "speed_factor": speed,
            "media_type": "wav",
            "streaming_mode": False,
        }

        # 4. 调用 API（HTTP 请求本身是线程安全的，Lock 仅护初始化 → M-01）
        client = self._get_client()
        try:
            resp = client.post("/tts", json=payload)
        except httpx.ConnectError:
            raise GPTSoVITSUnavailable("GPT-SoVITS server is unreachable")
        except httpx.TimeoutException:
            raise GPTSoVITSUnavailable("GPT-SoVITS request timed out")
        except httpx.HTTPError as e:  # M-02: 捕获 httpx 基类
            raise GPTSoVITSUnavailable(f"GPT-SoVITS HTTP error: {e}")

        # 5. 检查响应
        if resp.status_code == 400:
            err_body = resp.text[:200]
            logger.error("GPT-SoVITS API error (400): %s", err_body)  # M-04: 日志化，不暴露给客户端
            if "not found" in err_body.lower() or "ref_audio" in err_body.lower():
                raise GPTSoVITSNotFound("GPT-SoVITS: reference audio not found")
            raise GPTSoVITSAPIError("GPT-SoVITS API returned a bad request")
        if resp.status_code != 200:
            logger.error("GPT-SoVITS returned %s: %s", resp.status_code, resp.text[:200])
            raise GPTSoVITSAPIError(f"GPT-SoVITS returned status {resp.status_code}")

        # 6. 检查内容非空
        if not resp.content:
            raise GPTSoVITSAPIError("GPT-SoVITS returned empty response")

        # 7. 解析 wav → numpy（H-01: 防御式，捕获所有异常）
        try:
            audio, sr = sf.read(BytesIO(resp.content))
        except Exception as e:
            logger.error("Failed to parse GPT-SoVITS audio: %s", e)
            raise GPTSoVITSAPIError("GPT-SoVITS returned invalid audio data")

        # 8. 检查空音频
        if len(audio) == 0:
            raise GPTSoVITSAPIError("GPT-SoVITS returned empty audio")

        return sr, audio

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            with self._lock:
                if self._client is None:
                    self._client = httpx.Client(
                        base_url=self.base_url,
                        timeout=httpx.Timeout(self.timeout),
                        limits=httpx.Limits(
                            max_keepalive_connections=2,
                            max_connections=4,  # M-05: 合理值
                        ),
                    )
        return self._client
