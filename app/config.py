import base64
import tempfile
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_key: str = "change-me-before-deploy"
    tts_engine: str = "mock"
    output_format: str = "wav"
    max_text_chars: int = 1200
    default_language: str = "en"
    xtts_model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    voices_dir: Path = Path(__file__).resolve().parents[1] / "voices"
    jassi_voice_path: Path | None = None
    jassi_voice_base64: str | None = None

    @property
    def resolved_jassi_voice_path(self) -> Path:
        explicit_path = self.jassi_voice_path
        if explicit_path and explicit_path.exists():
            return explicit_path

        local_path = self.voices_dir / "jassi" / "voice_preview_jassi.mp3"
        if local_path.exists():
            return local_path

        if self.jassi_voice_base64:
            decoded_path = Path(tempfile.gettempdir()) / "voice_preview_jassi.mp3"
            if not decoded_path.exists():
                decoded_path.write_bytes(base64.b64decode(self.jassi_voice_base64))
            return decoded_path

        return explicit_path or local_path


@lru_cache
def get_settings() -> Settings:
    return Settings()