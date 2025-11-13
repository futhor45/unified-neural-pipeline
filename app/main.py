
import uvicorn
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from .pipeline import TargetDiarizationPipeline
from .models_config import DEFAULT_CONFIG
import os
import shutil
import asyncio

app = FastAPI(title="Unified Neural Pipeline")

pipeline = TargetDiarizationPipeline(DEFAULT_CONFIG)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process")
async def process(mixture: UploadFile = File(...), target: UploadFile = File(...)):
    mix_path = os.path.join(UPLOAD_DIR, mixture.filename)
    with open(mix_path, "wb") as f:
        f.write(await mixture.read())
    target_path = os.path.join(UPLOAD_DIR, target.filename)
    with open(target_path, "wb") as f:
        f.write(await target.read())
    outdir = os.path.join("outputs", os.path.splitext(mixture.filename)[0])
    result = await pipeline.process_offline(mix_path, target_path, outdir)
    return JSONResponse(result)

@app.websocket("/ws/stream")
async def websocket_stream(ws: WebSocket):
    await ws.accept()
    buffer = bytearray()
    try:
        while True:
            msg = await ws.receive_bytes()
            buffer.extend(msg)
            # process every ~3 seconds (demo)
            if len(buffer) > 16000 * 2 * 3:
                import tempfile, soundfile as sf, numpy as np
                tf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                samples = np.frombuffer(buffer, dtype='int16').astype('float32') / 32768.0
                sf.write(tf.name, samples, 16000)
                text, conf = pipeline.asr.transcribe(samples, 16000)
                await ws.send_json({"partial_text": text, "confidence": conf})
                buffer = bytearray()
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
