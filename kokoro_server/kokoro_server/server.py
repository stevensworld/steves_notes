import os
import io
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from kokoro import KPipeline

PORT = 4001

app = FastAPI()
pipeline = KPipeline(lang_code='a')
_output_dirs: dict = {}


class SynthesizeRequest(BaseModel):
    text: str
    voice: str = "af_heart"
    speed: float = 1.0
    job_id: str = "000"
    output_dir: str = "."


@app.get("/health")
def health():
    return {"status": "ready"}


@app.post("/synthesize")
def synthesize(req: SynthesizeRequest):
    job_dir = os.path.join(req.output_dir, req.job_id)
    os.makedirs(job_dir, exist_ok=True)
    _output_dirs[req.job_id] = req.output_dir

    generator = pipeline(
        req.text,
        voice=req.voice,
        speed=req.speed,
        split_pattern=r'\n+',
    )

    files = []
    for i, (gs, ps, audio) in enumerate(generator):
        wav_buf = io.BytesIO()
        sf.write(wav_buf, audio, 24000, format="WAV")
        wav_buf.seek(0)
        segment = AudioSegment.from_wav(wav_buf)
        filename = f"{i:05}.mp3"
        filepath = os.path.join(job_dir, filename)
        segment.export(filepath, format="mp3")
        files.append(filename)

    return {"job_id": req.job_id, "files": files, "output_dir": job_dir}


@app.get("/download/{job_id}/{filename}")
def download(job_id: str, filename: str):
    filepath = os.path.join(_output_dirs.get(job_id, "."), job_id, filename)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail=f"File not found: {filepath}")
    return FileResponse(filepath, media_type="audio/mpeg", filename=filename)


def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    run()
