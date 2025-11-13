
import webrtcvad
import numpy as np
import soundfile as sf

class VoiceActivityDetector:
    def __init__(self, cfg):
        self.vad = webrtcvad.Vad(cfg.get("mode", 2))

    def wav_to_frames(self, audio, sr, frame_duration_ms=30):
        audio_int16 = (audio * 32767).astype('int16')
        frame_bytes = audio_int16.tobytes()
        frame_size = int(sr * frame_duration_ms / 1000) * 2
        frames = []
        for i in range(0, len(frame_bytes), frame_size):
            frames.append(frame_bytes[i:i+frame_size])
        return frames, frame_duration_ms / 1000.0

    def get_speech_regions(self, audio, sr):
        frames, frame_dur = self.wav_to_frames(audio, sr)
        speech_flags = [bool(self.vad.is_speech(f, sr)) for f in frames]
        regions = []
        start = None
        for i, flag in enumerate(speech_flags):
            t = i * frame_dur
            if flag and start is None:
                start = t
            if not flag and start is not None:
                regions.append({"start": start, "end": t})
                start = None
        if start is not None:
            regions.append({"start": start, "end": len(frames)*frame_dur})
        return regions
