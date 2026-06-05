from pydantic import BaseModel, Field, field_validator


class VoiceProfile(BaseModel):
    id: str
    display_name: str
    language: str
    reference_audio: str
    ready: bool


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1200)
    voice: str = "jassi"
    language: str | None = None
    style: str | None = Field(default=None, max_length=240)
    speed: float = Field(default=1.0, ge=0.5, le=1.5)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty.")
        return value
