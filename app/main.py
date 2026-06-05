from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.responses import Response

from .config import Settings, get_settings
from .engine import TTSEngine
from .schemas import TTSRequest, VoiceProfile
from .security import require_api_key

app = FastAPI(
    title="Jassi Custom Voice TTS API",
    version="0.1.0",
    description="Self-managed hosted TTS API for a private Jassi voice reference.",
)


@lru_cache
def get_engine() -> TTSEngine:
    return TTSEngine(get_settings())


@app.get("/health")
def health(settings: Settings = Depends(get_settings)) -> dict[str, object]:
    return {
        "status": "ok",
        "engine": settings.tts_engine,
        "voice_reference_ready": settings.resolved_jassi_voice_path.exists(),
        "output_format": settings.output_format,
    }


@app.get("/voices", dependencies=[Depends(require_api_key)])
def voices(settings: Settings = Depends(get_settings)) -> list[VoiceProfile]:
    return [
        VoiceProfile(
            id="jassi",
            display_name="Jassi Custom Voice",
            language=settings.default_language,
            reference_audio=str(settings.resolved_jassi_voice_path),
            ready=settings.resolved_jassi_voice_path.exists(),
        )
    ]


@app.post("/tts", dependencies=[Depends(require_api_key)])
def tts(
    request: TTSRequest,
    engine: TTSEngine = Depends(get_engine),
) -> Response:
    audio, media_type = engine.synthesize(request)
    extension = "wav" if media_type == "audio/wav" else "mp3"
    return Response(
        content=audio,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="jassi_tts.{extension}"'},
    )
