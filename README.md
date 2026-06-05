# Jassi Custom Voice TTS API

Self-managed FastAPI TTS API for your private `jassi` voice reference.

## Status

Working now:

```text
FastAPI API scaffold
Private X-API-Key authentication
/health, /voices, /tts endpoints
Jassi reference audio attached
Python 3.10 XTTS environment
Coqui TTS / XTTS installed
XTTS model downloaded
Real Jassi voice generation tested
Real /tts API endpoint tested
```

Generated test files:

```text
test_jassi_xtts.wav      direct XTTS generation test
test_jassi_api_xtts.wav  FastAPI /tts endpoint test
```

## Important Runtime Notes

The local installed XTTS environment is:

```text
.venv-xtts
Python 3.10.20
TTS==0.22.0
transformers==4.40.2
torch==2.1.2
```

Do not upgrade `transformers` to 5.x or PyTorch to a newer weights-only default build without testing; XTTS failed with those versions.

## Run The API

PowerShell:

```powershell
$env:COQUI_TOS_AGREED="1"
.\.venv-xtts\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Call it:

```powershell
curl.exe -X POST "http://127.0.0.1:8080/tts" `
  -H "X-API-Key: YOUR_PRIVATE_KEY" `
  -H "Content-Type: application/json" `
  -d "{\"text\":\"Hi dear, this is Jassi speaking.\",\"voice\":\"jassi\",\"language\":\"en\",\"style\":\"Speak naturally in a warm female voice.\"}" `
  --output jassi.wav
```

## Reinstall XTTS If Needed

```powershell
.\.venv\Scripts\uv.exe python install 3.10
.\.venv\Scripts\uv.exe venv .venv-xtts --python 3.10
.\.venv\Scripts\uv.exe pip install --python .\.venv-xtts\Scripts\python.exe -r requirements.txt -r requirements-xtts.txt
```

## Cloud Later

For always-on use when your computer is off, deploy this folder to a GPU-capable host:

```text
RunPod GPU pod
Vast.ai GPU instance
Hugging Face Space GPU
Google Cloud GPU VM
```

CPU works but is slow. In local CPU testing, a short API request took around 90 seconds including model load. A running server caches the model after first request, but GPU is recommended.

Keep your API key and voice file private. Only clone voices you own or have permission to use.
