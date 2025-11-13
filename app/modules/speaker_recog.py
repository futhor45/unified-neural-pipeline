
# Lightweight speaker recognizer using MFCC mean as embedding (demo).
import numpy as np
from scipy.spatial.distance import cosine
import librosa

class SpeakerRecognizer:
    def __init__(self, cfg):
        self.cfg = cfg

    def mfcc_embedding(self, audio, sr):
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
        return mfcc.mean(axis=1)

    def get_embedding(self, audio, sr):
        return self.mfcc_embedding(audio, sr)

    def similarity(self, emb1, emb2):
        d = cosine(emb1, emb2)
        sim = 1 - d
        return max(0.0, min(1.0, sim))
