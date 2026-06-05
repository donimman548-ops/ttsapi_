import math
import struct
import tempfile
import wave
from pathlib import Path

from fastapi import HTTPException, status

from .config import Settings
from .schemas import TTSRequest


class TTSEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._xtts = None

    def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        if request.voice != "jassi":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unknown voice '{request.voice}'. Available voice: jassi.",
            )

        if not self.settings.resolved_jassi_voice_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Jassi reference audio is missing. Put it at voices/jassi/voice_preview_jassi.mp3.",
            )

        if self.settings.tts_engine.lower() == "xtts":
            return self._synthesize_xtts(request), "audio/wav"

        return self._synthesize_mock(request), "audio/wav"

    def _synthesize_xtts(self, request: TTSRequest) -> bytes:
        try:
            from TTS.api import TTS
        except ImportError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="TTS package is not installed. Install XTTS dependencies or set TTS_ENGINE=mock.",
            ) from exc

        if self._xtts is None:
            self._xtts = TTS(self.settings.xtts_model_name)

        language = request.language or self.settings.default_language
        text = self._styled_text(request)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            self._xtts.tts_to_file(
                text=text,
                speaker_wav=str(self.settings.resolved_jassi_voice_path),
                language=language,
                file_path=str(output_path),
            )
            return output_path.read_bytes()
        finally:
            output_path.unlink(missing_ok=True)

    def _synthesize_mock(self, request: TTSRequest) -> bytes:
        # Lightweight validation audio so API behavior can be tested without downloading a model.
        duration = min(max(len(request.text) / 35.0, 0.8), 4.0)
        sample_rate = 22050
        frequency = 180.0
        frames = int(duration * sample_rate)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            with wave.open(str(output_path), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(sample_rate)
                for index in range(frames):
                    fade = min(index / 1000, (frames - index) / 1000, 1.0)
                    sample = int(9000 * fade * math.sin(2 * math.pi * frequency * index / sample_rate))
                    wav.writeframes(struct.pack("<h", sample))
            return output_path.read_bytes()
        finally:
            output_path.unlink(missing_ok=True)

    def _styled_text(self, request: TTSRequest) -> str:
        if not request.style:
            return request.text
        return f"{request.style.strip()}\n\n{request.text}"
