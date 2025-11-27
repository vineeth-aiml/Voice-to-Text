from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
TRANSCRIPTS_DIR = OUTPUTS_DIR / "transcripts"
LOGS_DIR = OUTPUTS_DIR / "logs"

# Create required folders
for p in (MODELS_DIR, TRANSCRIPTS_DIR, LOGS_DIR):
    os.makedirs(p, exist_ok=True)

# Model paths
VOSK_DEFAULT_MODEL = MODELS_DIR / "vosk-model-small-en-us-0.15"
WHISPER_GGML_BIN = MODELS_DIR / "whisper-ggml" / "ggml-base.en.bin"
