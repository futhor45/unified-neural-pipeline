
DEFAULT_CONFIG = {
    "vad": {"mode": 2},
    "denoise": {},
    "separator": {},
    "speaker_recog": {},
    "diarizer": {"model": "pyannote/speaker-diarization"},
    "asr": {"model": "small", "use_cuda": False},
    "punct": {"model": "oliverguhr/fullstop-punctuation-multilingual"},
    "target_threshold": 0.70
}
