import subprocess
from pathlib import Path
from typing import Optional

class WhisperRecognizer:
    def __init__(self, model_bin: str, whisper_exec: Optional[str] = None):
        self.model_bin = Path(model_bin)
        if not self.model_bin.exists():
            raise FileNotFoundError(f"Whisper GGML file not found: {self.model_bin}")

        self.whisper_exec = whisper_exec or "main"

    def transcribe_file(self, wav_path: str, language="en"):
        cmd = f'{self.whisper_exec} -m "{self.model_bin}" -f "{wav_path}" -otxt -l {language}'
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if proc.returncode != 0:
            raise RuntimeError(proc.stderr)

        out_txt = Path(wav_path).with_suffix(".txt")
        if out_txt.exists():
            return out_txt.read_text(encoding="utf-8").strip()

        return proc.stdout.strip()
