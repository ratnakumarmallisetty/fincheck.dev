from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import aiofiles
import json

from msgqueue.connection import get_connection
import pika

app = FastAPI(title="FASTAPI BACKEND", version="1.1.0")

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FastAPI is running.."}


@app.get("/health")
def health_check():
    return {"message": "ok", "service": "backend"}


def publish_inference_job(job_id: str, filepath: str):
    try:
        conn = get_connection()
        ch = conn.channel()

        ch.queue_declare(queue="model_queue", durable=True)

        msg = json.dumps({"job_id": job_id, "filepath": filepath})

        ch.basic_publish(
            exchange="",
            routing_key="model_queue",
            body=msg,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[Backend] Job published → {job_id}")
        conn.close()

    except Exception as e:
        print("[Backend] Error publishing:", e)
        raise HTTPException(status_code=500, detail="Message queue error")


@app.post("/upload-image")
async def image_upload(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")

    total_size = 0
    CHUNK_SIZE = 1024 * 1024

    while chunk := await file.read(CHUNK_SIZE):
        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File exceeds max size 5MB")

    await file.seek(0)

    ext = file.filename.split(".")[-1]
    saved_name = f"{uuid.uuid4()}.{ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)

    async with aiofiles.open(saved_path, "wb") as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)

    await file.close()

    job_id = str(uuid.uuid4())
    publish_inference_job(job_id, saved_path)

    return {
        "message": "Image uploaded successfully",
        "job_id": job_id,
        "filepath": saved_path,
        "mime_type": file.content_type,
        "size": total_size,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)