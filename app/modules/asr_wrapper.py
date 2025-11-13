
# ASR wrapper using faster-whisper if available.
import numpy as np

class ASR:
    def __init__(self, cfg):
        self.backend = "none"
        self.model = None
        self.cfg = cfg
        model = cfg.get("model", "small")
        try:
            from faster_whisper import WhisperModel
            device = "cuda" if cfg.get("use_cuda", False) else "cpu"
            self.model = WhisperModel(model, device=device)
            self.backend = "faster_whisper"
        except Exception as e:
            print("Warning: faster-whisper not available:", e)
            self.backend = "none"

    def transcribe(self, audio, sr):
        if self.backend == "faster_whisper":
            import tempfile, soundfile as sf
            tf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            sf.write(tf.name, audio, sr)
            segments, info = self.model.transcribe(tf.name, beam_size=5)
            text = " ".join([seg.text for seg in segments])
            conf = info.get("avg_logprob", 0.0)
            return text, conf
        # Fallback: return empty text with confidence 0
        return "", 0.0
