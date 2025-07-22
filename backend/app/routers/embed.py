from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from backend.app.models.embed import EmbedderResponse
from backend.app.services.embed.embedder import get_embeddings

router = APIRouter()


@router.post("/embed")
async def embed_image_text(
    image: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
):
    if image is None and text is None:
        raise HTTPException(
            status_code=400, detail="Either image or text must be provided."
        )
    image_bytes = await image.read() if image else None
    result: EmbedderResponse = get_embeddings(image_bytes, text)
    return JSONResponse(content=result.model_dump())


# with open("your_image.jpg", "rb") as f:
#     response = requests.post("http://localhost:8000/embed", files={"image": f}, data={"text": "a photo of a cat"})
