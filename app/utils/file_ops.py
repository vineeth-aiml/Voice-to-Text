from datetime import datetime
import uuid
from pathlib import Path
from app.core.config import TRANSCRIPTS_DIR

def save_transcript(text: str, source="unknown") -> str:
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{ts}_{source}_{uuid.uuid4().hex[:6]}.txt"
    path = Path(TRANSCRIPTS_DIR) / filename
    path.write_text(text, encoding="utf-8")
    return str(path)
