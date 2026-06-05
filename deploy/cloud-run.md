# Google Cloud Run Deployment

Cloud Run is good for the API wrapper. Real XTTS voice cloning is heavy and may need a GPU runtime; use Cloud Run only after confirming the selected runtime can run your model fast enough.

1. Create a private API key value and keep it secret.
2. Build the container:

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT/jassi-tts-api
```

3. Deploy:

```bash
gcloud run deploy jassi-tts-api \
  --image gcr.io/YOUR_PROJECT/jassi-tts-api \
  --region asia-south1 \
  --set-env-vars API_KEY=YOUR_PRIVATE_KEY,TTS_ENGINE=mock \
  --allow-unauthenticated
```

4. Call it:

```bash
curl -X POST "https://YOUR_SERVICE_URL/tts" \
  -H "X-API-Key: YOUR_PRIVATE_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hey dear, how are you?\",\"voice\":\"jassi\",\"language\":\"en\"}" \
  --output jassi.wav
```

For real cloned voice output, install XTTS dependencies in the image and set `TTS_ENGINE=xtts`.
