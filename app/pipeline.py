
import asyncio
import json
import os
from .modules.vad import VoiceActivityDetector
from .modules.denoise import Denoiser
from .modules.separator import Separator
from .modules.speaker_recog import SpeakerRecognizer
from .modules.diarization_wrapper import Diarizer
from .modules.asr_wrapper import ASR
from .modules.punctuation import Punctuator
from .utils import load_wav, save_wav

class TargetDiarizationPipeline:
    def __init__(self, config):
        self.vad = VoiceActivityDetector(config.get("vad", {}))
        self.denoiser = Denoiser(config.get("denoise", {}))
        self.separator = Separator(config.get("separator", {}))
        self.speaker_recog = SpeakerRecognizer(config.get("speaker_recog", {}))
        self.diarizer = Diarizer(config.get("diarizer", {}))
        self.asr = ASR(config.get("asr", {}))
        self.punct = Punctuator(config.get("punct", {}))
        self.config = config

    async def process_offline(self, mixture_path, target_ref_path, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        audio, sr = load_wav(mixture_path)
        # 1. Denoise
        cleaned = self.denoiser.denoise(audio, sr)
        # 2. VAD -> speech segments (not used directly for diarization here)
        segments = self.vad.get_speech_regions(cleaned, sr)
        # 3. Optional: full audio separation
        separated = self.separator.separate(cleaned, sr)
        # 4. Extract target embedding
        target_wav, _ = load_wav(target_ref_path)
        target_emb = self.speaker_recog.get_embedding(target_wav, sr)
        # 5. Diarization to get speaker turns
        diarization = self.diarizer.run_diarization(cleaned, sr)
        # 6. Map diarization speakers to "Target" if similarity to target_emb
        results = []
        for turn in diarization:
            start, end, speaker = turn["start"], turn["end"], turn["speaker"]
            seg_audio = cleaned[int(start * sr): int(end * sr)]
            emb = self.speaker_recog.get_embedding(seg_audio, sr)
            sim = self.speaker_recog.similarity(emb, target_emb)
            label = "Target" if sim >= self.config.get("target_threshold", 0.7) else speaker
            # 7. ASR
            text, conf = self.asr.transcribe(seg_audio, sr)
            text = self.punct.restore(text)
            results.append({
                "speaker": label,
                "start": start,
                "end": end,
                "text": text,
                "confidence": conf,
                "similarity": float(sim)
            })
        # write JSON
        out_json = os.path.join(output_dir, "diarization.json")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        # optionally write isolated target_speaker.wav by concatenating target-labeled segments
        target_segments = [r for r in results if r["speaker"] == "Target"]
        target_audio = self.separator.extract_target_audio(cleaned, sr, target_segments)
        save_wav(os.path.join(output_dir, "target_speaker.wav"), target_audio, sr)
        return {"json": out_json, "target_wav": os.path.join(output_dir, "target_speaker.wav")}
