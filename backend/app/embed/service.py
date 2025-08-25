import io

from app.embed.clipembedder import get_clip_embedder
from fastapi import UploadFile
from PIL import Image
from PIL.ImageFile import ImageFile


def get_text_embeddings(text: str) -> list[float]:
    return get_clip_embedder().embed_query(text)


def get_image_file_embeddings(image: ImageFile) -> list[float]:
    return get_clip_embedder().encode_image(image)


async def get_image_uploadfile_embeddings(file: UploadFile) -> list[float]:
    contents = await file.read()
    image: ImageFile = Image.open(io.BytesIO(contents)).convert("RGB")
    return get_clip_embedder().encode_image(image)
