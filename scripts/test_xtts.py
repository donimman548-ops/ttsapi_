from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.engine import TTSEngine
from app.schemas import TTSRequest

settings = get_settings()
print(f"engine={settings.tts_engine}")
print(f"voice_reference={settings.jassi_voice_path}")
print(f"voice_reference_ready={settings.jassi_voice_path.exists()}")

request = TTSRequest(
    text="Hello dear, this is the real Jassi voice clone test.",
    voice="jassi",
    language="en",
    style="Speak in a deep, warm, natural female voice with relaxed pacing.",
    speed=0.9,
)

audio, media_type = TTSEngine(settings).synthesize(request)
out = ROOT / ("test_jassi_xtts.wav" if settings.tts_engine == "xtts" else "test_jassi_mock.wav")
out.write_bytes(audio)
print(f"media_type={media_type}")
print(f"bytes={len(audio)}")
print(f"saved={out.resolve()}")
