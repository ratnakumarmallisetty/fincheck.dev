from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import aiofiles

app = FastAPI(title="FASTAPI BACKEND", version="1.0.0")

# Allowed image types
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

# Max file size = 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production, set your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home page
@app.get("/")
def home():
    return {"message": "FastAPI is running.."}


# Health check
@app.get("/health")
def health_check():
    return {"message": "ok", "service": "backend"}


@app.post("/upload-image")
async def image_upload(file: UploadFile = File(...)):
    #  Validate extension/type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type..")

    #  Validate by reading chunks
    total_size = 0
    CHUNK_SIZE = 1024 * 1024  # 1 MB per chunk

    while chunk := await file.read(CHUNK_SIZE):
        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Exceeding max file size..")

    # Reset cursor to re-read file for saving
    await file.seek(0)

    #  Save file to uploads folder
    ext = file.filename.split(".")[-1]
    saved_name = f"{uuid.uuid4()}.{ext}"
    saved_path = os.path.join("uploads", saved_name)

    os.makedirs("uploads", exist_ok=True)

    async with aiofiles.open(saved_path, "wb") as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)

    #  Metadata
    metadata = {
        "original_name": file.filename,
        "saved_name": saved_name,
        "mime_type": file.content_type,
        "size_bytes": total_size,
        "path": saved_path,
    }

    await file.close()

    return JSONResponse(
        status_code=201,
        content={"message": "Image upload successful", "metadata": metadata},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
