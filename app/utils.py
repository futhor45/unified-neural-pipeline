
import soundfile as sf
import numpy as np
import os

def load_wav(path):
    data, sr = sf.read(path)
    # ensure float32
    if data.dtype != 'float32':
        data = data.astype('float32')
    # if stereo, convert to mono
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    return data, sr

def save_wav(path, audio, sr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, audio, sr)
