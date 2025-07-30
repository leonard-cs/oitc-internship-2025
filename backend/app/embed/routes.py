import os
import shutil
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from backend.app.embed.models import EmbedderResponse
from backend.app.embed.clipembedder import CLIPEmbedder
from backend.app.embed.service import get_embeddings

router = APIRouter()


@router.post("/embed")
async def embed_image_text(
    image: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
):
    image_bytes = await image.read() if image else None
    result: EmbedderResponse = get_embeddings(image_bytes, text)
    return JSONResponse(content=result.model_dump())


# with open("your_image.jpg", "rb") as f:
#     response = requests.post("http://localhost:8000/embed", files={"image": f}, data={"text": "a photo of a cat"})


@router.post("/embed-image")
async def embed_image(file: UploadFile = File(...)) -> list[float]:
    image_path = _file_preprocess(file)
    embedder = CLIPEmbedder()
    embedding = embedder.embed_query(image_path)
    os.remove(image_path)
    return embedding


def _file_preprocess(file: UploadFile = File(...)) -> str:
    image_path = f"temp_{file.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return image_path
