import streamlit as st
from pathlib import Path
import tempfile
import numpy as np
from scipy.io.wavfile import write
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase

from app.core.audio_processor import ensure_wav_mono_16k
from app.core.vosk_recognizer import VoskRecognizer
from app.core.whisper_recognizer import WhisperRecognizer
from app.core.config import MODELS_DIR
from app.utils.file_ops import save_transcript

st.set_page_config(page_title="Voice to Text", layout="wide")
st.title("🎙 Voice → Text Transcription (Offline)")

engine = st.sidebar.selectbox("Engine", ["vosk", "whisper"])
lang = st.sidebar.text_input("Language", "en-US")
save_opt = st.sidebar.checkbox("Save transcripts", True)

tabs = st.tabs(["Dictate", "Upload", "Settings"])

# -------------------------
# 1) Dictate
# -------------------------
class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame):
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame


with tabs[0]:
    st.header("Live Dictation")

    ctx = webrtc_streamer(
        key="dictate",
        mode="sendonly",
        audio_processor_factory=AudioRecorder,
        media_stream_constraints={"audio": True, "video": False}
    )

    if st.button("Stop & Transcribe") and ctx.audio_processor:
        frames = np.concatenate(ctx.audio_processor.frames, axis=0)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        write(tmp.name, 16000, frames)
        wav_path = ensure_wav_mono_16k(tmp.name)

        if engine == "vosk":
            rec = VoskRecognizer(MODELS_DIR / "vosk-model-small-en-us-0.15")
            text = rec.transcribe_file(wav_path)
        else:
            rec = WhisperRecognizer(MODELS_DIR / "whisper-ggml" / "ggml-base.en.bin")
            text = rec.transcribe_file(wav_path, language=lang)

        st.text_area("Transcript", text, height=300)

        if save_opt:
            path = save_transcript(text, source="dictate")
            st.success(f"Saved: {path}")

# -------------------------
# 2) Upload
# -------------------------
with tabs[1]:
    st.header("Upload Audio File")

    up = st.file_uploader("Upload audio", type=["wav", "mp3", "ogg", "m4a", "flac"])
    if up:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(up.read())
        tmp.flush()

        wav_path = ensure_wav_mono_16k(tmp.name)
        st.audio(wav_path)

        if st.button("Transcribe Upload"):
            if engine == "vosk":
                rec = VoskRecognizer(MODELS_DIR / "vosk-model-small-en-us-0.15")
                text = rec.transcribe_file(wav_path)
            else:
                rec = WhisperRecognizer(MODELS_DIR / "whisper-ggml" / "ggml-base.en.bin")
                text = rec.transcribe_file(wav_path, language=lang)

            st.text_area("Transcript", text, height=300)

            if save_opt:
                path = save_transcript(text, source="upload")
                st.success(f"Saved: {path}")

# -------------------------
# 3) Settings
# -------------------------
with tabs[2]:
    st.header("Settings")
    st.write(f"Models folder: `{MODELS_DIR}`")
