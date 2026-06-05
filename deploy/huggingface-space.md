# Hugging Face Space Deployment

Hugging Face Spaces can host this as a Docker Space. CPU Spaces are usually slow for voice cloning; GPU Spaces are better for XTTS/OpenVoice/F5-TTS.

Recommended Space settings:

```text
SDK: Docker
Secret: API_KEY
Variable: TTS_ENGINE=mock or xtts
Hardware: GPU for real cloning
```

Upload the `voice_tts_api` folder as the Space contents. Keep `voices/jassi/voice_preview_jassi.mp3` private if the voice should not be public.

API call:

```bash
curl -X POST "https://YOUR_SPACE.hf.space/tts" \
  -H "X-API-Key: YOUR_PRIVATE_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"I am speaking with the Jassi voice.\",\"voice\":\"jassi\"}" \
  --output jassi.wav
```
