import io

from app.embed.clipembedder import get_clip_embedder
from fastapi import UploadFile
from PIL import Image
from PIL.ImageFile import ImageFile


def get_text_embeddings(text: str) -> list[float]:
    return get_clip_embedder().encode_text(text)


async def handle_image_embed(file: UploadFile) -> list[float]:
    contents = await file.read()
    image: ImageFile = Image.open(io.BytesIO(contents)).convert("RGB")
    return get_clip_embedder().encode_image(image)
