import threading
from abc import ABC, abstractmethod

import numpy as np


class TTSEngine(ABC):
    @abstractmethod
    def generate(self, text: str, voice: str, **kwargs) -> tuple[int, np.ndarray]:
        ...


class KokoroAdapter(TTSEngine):
    def __init__(self, lang_code: str = "a", device: str = "auto"):
        from utilities.speech_generator import SpeechGenerator

        self.sg = SpeechGenerator(lang_code=lang_code, device=device)
        self._lock = threading.Lock()

    def generate(self, text: str, voice: str, speed: float = 1.0, **kwargs) -> tuple[int, np.ndarray]:
        with self._lock:
            audio = self.sg.generate_audio(text, voice, speed)
        return 24000, audio
