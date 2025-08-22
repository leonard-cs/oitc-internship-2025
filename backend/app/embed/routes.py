from app.embed.service import get_text_embeddings, handle_image_embed
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

router = APIRouter()


@router.post("/embed-text", summary="Generate embeddings for text")
async def embed_image_text(
    text: str = Form(..., description="Text to embed"),
) -> list[float]:
    """
    Generate CLIP embeddings for text inputs.

    This endpoint accepts either an image file, text string, or both and returns:
    - Text embedding (512-dimensional vector)
    - Cosine similarity between image and text (if both provided)

    Args:
        text: Optional text string to embed

    Returns:
        EmbedderResponse containing embeddings and similarity score
    """
    try:
        return await get_text_embeddings(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
