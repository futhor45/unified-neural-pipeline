"""
Safe diarization wrapper: attempts to import pyannote.audio at runtime.
If pyannote is not available, uses a simple fallback that returns a single speaker
covering the entire audio, so the app keeps running for demo purposes.
"""
import tempfile, os, soundfile as sf

try:
    from pyannote.audio import Pipeline
    _HAS_PYANNOTE = True
except Exception as _e:
    # pyannote not installed or failed to load
    _HAS_PYANNOTE = False

class Diarizer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.pipeline = None
        if _HAS_PYANNOTE:
            model_name = cfg.get("model", "pyannote/speaker-diarization")
            try:
                self.pipeline = Pipeline.from_pretrained(model_name)
            except Exception as e:
                print("Warning: pyannote pipeline failed to load at runtime:", e)
                self.pipeline = None

    def run_diarization(self, audio, sr):
        # write temp file
        tf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tf.name, audio, sr)
        tf.close()

        turns = []
        if self.pipeline:
            try:
                diarization = self.pipeline(tf.name)
                for turn, track, speaker in diarization.itertracks(yield_label=True):
                    turns.append({"start": round(turn.start,3), "end": round(turn.end,3), "speaker": speaker})
            except Exception as e:
                print("Warning: pyannote pipeline failed during run:", e)
                self.pipeline = None

        if not turns:
            # fallback: single speaker segment covering whole audio
            info = sf.info(tf.name)
            duration = info.frames / info.samplerate
            turns.append({"start": 0.0, "end": float(duration), "speaker": "Speaker_0"})

        try:
            os.unlink(tf.name)
        except Exception:
            pass
        return turns
