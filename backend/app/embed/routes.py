from typing import Optional

from app.embed.models import EmbedderResponse
from app.embed.service import get_embeddings, handle_image_embed
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
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


@router.post("/embed-image", summary="Generate embedding for image")
async def embed_image(
    file: UploadFile = File(..., description="Image file to embed"),
) -> list[float]:
    """
    Generate CLIP embedding for a single image file.

    This endpoint accepts an image file and returns the image embedding
    as a 512-dimensional vector. This is a simpler alternative to the /embed
    endpoint when you only need image embeddings without text processing.

    Args:
        file: Image file (JPEG, PNG, etc.) - required

    Returns:
        List of 512 float values representing the image embedding
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")

    try:
        return await handle_image_embed(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
