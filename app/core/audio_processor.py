from pydub import AudioSegment
import tempfile
from pathlib import Path

def ensure_wav_mono_16k(path: str) -> str:
    p = Path(path)
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    out.close()

    audio = AudioSegment.from_file(str(p))
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(out.name, format="wav")

    return out.name
