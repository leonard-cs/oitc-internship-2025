import os
import shutil
from typing import Optional

from app.embed.clipembedder import CLIPEmbedder
from app.embed.models import EmbedderResponse
from app.embed.service import get_embeddings
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/embed", summary="Generate embeddings for image and/or text")
async def embed_image_text(
    image: Optional[UploadFile] = File(default=None, description="Image file to embed"),
    text: Optional[str] = Form(default=None, description="Text to embed"),
):
    """
    Generate CLIP embeddings for image and/or text inputs.

    This endpoint accepts either an image file, text string, or both and returns:
    - Image embedding (512-dimensional vector)
    - Text embedding (512-dimensional vector)
    - Cosine similarity between image and text (if both provided)

    Args:
        image: Optional image file (JPEG, PNG, etc.)
        text: Optional text string to embed

    Returns:
        EmbedderResponse containing embeddings and similarity score
    """
    image_bytes = await image.read() if image else None
    result: EmbedderResponse = get_embeddings(image_bytes, text)
    return JSONResponse(content=result.model_dump())


# with open("your_image.jpg", "rb") as f:
#     response = requests.post("http://localhost:8000/embed", files={"image": f}, data={"text": "a photo of a cat"})


@router.post("/embed-image", summary="Generate embedding for image only")
async def embed_image(
    file: UploadFile = File(..., description="Image file to embed"),
) -> list[float]:
    """
    Generate CLIP embedding for a single image file.

    This endpoint accepts an image file and returns only the image embedding
    as a 512-dimensional vector. This is a simpler alternative to the /embed
    endpoint when you only need image embeddings without text processing.

    Args:
        file: Image file (JPEG, PNG, etc.) - required

    Returns:
        List of 512 float values representing the image embedding

    Note:
        The image is temporarily saved to disk during processing and
        automatically cleaned up after embedding generation.
    """
    image_path = _file_preprocess(file)
    embedder = CLIPEmbedder()
    embedding = embedder.embed_query(image_path)
    os.remove(image_path)
    return embedding


def _file_preprocess(file: UploadFile = File(...)) -> str:
    """
    Preprocess uploaded file by saving it temporarily to disk.

    Args:
        file: The uploaded file from FastAPI

    Returns:
        str: Path to the temporary file on disk

    Note:
        The caller is responsible for cleaning up the temporary file
        after processing is complete.
    """
    image_path = f"temp_{file.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return image_path
