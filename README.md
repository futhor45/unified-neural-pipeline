
# 🎤 Target Speaker Extraction + Diarization + WhisperX ASR
A complete end-to-end audio intelligence pipeline built with:

- WhisperX ASR
- WhisperX Diarization
- Silero VAD
- SpeechBrain ECAPA Speaker Embeddings
- FastAPI backend
- UI upload page
- Fully compatible with macOS ARM (M1/M2/M3)

## 🚀 Run the server

cd unified-neural-pipeline
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## 🧪 Test API using cURL

curl -F "mixture=@mixture.wav" -F "target=@target.wav" http://localhost:8000/process

## 🖥️ Use the UI

open ui/static_upload.html

Upload:
- mixture_audio.wav  
- target_sample.wav

Click **Process** to get JSON + extracted target audio.

## 📂 Output Structure

outputs/
  mixture_audio/
    seg_0.00.wav
    seg_2.50.wav
    target_speaker.wav
    diarization.json

## 🧠 Architecture Overview

Target sample
     ↓ (SpeechBrain ECAPA Embedding)
WhisperX Diarization + Silero VAD
     ↓ (Speaker Similarity Scoring)
Extracted target speech + JSON result

## 🧑‍💻 Technologies Used
FastAPI • WhisperX • Faster-Whisper • SpeechBrain ECAPA • Silero VAD • Torch MPS • Python 3.11

