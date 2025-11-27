from vosk import Model, KaldiRecognizer
import wave, json
from pathlib import Path

class VoskRecognizer:
    def __init__(self, model_path: str):
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Vosk model not found: {model_path}")

        self.model = Model(str(model_path))

    def transcribe_file(self, wav_path: str) -> str:
        wf = wave.open(wav_path, "rb")
        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)

        transcript = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break

            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                transcript.append(res.get("text", ""))

        final = json.loads(rec.FinalResult()).get("text", "")
        transcript.append(final)

        return " ".join(transcript).strip()
