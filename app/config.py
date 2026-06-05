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

    @property
    def jassi_voice_path(self) -> Path:
        return self.voices_dir / "jassi" / "voice_preview_jassi.mp3"


@lru_cache
def get_settings() -> Settings:
    return Settings()
