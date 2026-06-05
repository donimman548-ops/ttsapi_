# Render Free Deployment

Render free web services can deploy the API wrapper, but they are not suitable for real XTTS voice cloning. XTTS needs large model files and high memory/compute; the free Render build can fail when installing `torch`, `torchaudio`, and `TTS`.

This repository's `render.yaml` is therefore configured for a safe free deploy:

```text
buildCommand: pip install -r requirements.txt
TTS_ENGINE=mock
```

That means Render can expose `/health`, `/voices`, and `/tts`, but `/tts` returns validation audio, not the real Jassi cloned voice.

For real Jassi voice output, run locally with `.venv-xtts` or deploy on a GPU-capable service such as RunPod, Vast.ai, or a GPU VM.

Render environment variables for the free deploy:

```env
API_KEY=your_private_key
TTS_ENGINE=mock
DEFAULT_LANGUAGE=en
MAX_TEXT_CHARS=1200
```

Do not upload `.env`, `.env.render.full`, voice samples, generated WAV files, or model files to a public repository.
