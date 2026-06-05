from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "app/main.py",
    "app/config.py",
    "app/engine.py",
    "app/security.py",
    "app/schemas.py",
    "requirements.txt",
    "Dockerfile",
    ".env.example",
    "voices/jassi/voice_preview_jassi.mp3",
    "deploy/cloud-run.md",
    "deploy/huggingface-space.md",
    "README.md",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")

    main_py = (ROOT / "app" / "main.py").read_text(encoding="utf-8")
    for route in ['@app.get("/health")', '@app.get("/voices"', '@app.post("/tts"']:
        if route not in main_py:
            raise SystemExit(f"Missing route declaration: {route}")

    security_py = (ROOT / "app" / "security.py").read_text(encoding="utf-8")
    if "X-API-Key" not in security_py:
        raise SystemExit("API key header check is missing.")

    voice_size = (ROOT / "voices" / "jassi" / "voice_preview_jassi.mp3").stat().st_size
    if voice_size < 100_000:
        raise SystemExit("Voice reference file is too small or was not copied correctly.")

    print("voice_tts_api validation passed")


if __name__ == "__main__":
    main()
