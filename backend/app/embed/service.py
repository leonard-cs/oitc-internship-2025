import io

import open_clip
import torch
from app.embed.clipembedder import CLIPEmbedder
from fastapi import UploadFile
from PIL import Image
from PIL.ImageFile import ImageFile

model = None
preprocess = None
tokenizer = None


def handle_text_embed(text: str) -> list[float]:
    return CLIPEmbedder().encode_text(text)


async def handle_image_embed(file: UploadFile) -> list[float]:
    contents = await file.read()
    image: ImageFile = Image.open(io.BytesIO(contents)).convert("RGB")
    return CLIPEmbedder().encode_image(image)


def load_model():
    global model, preprocess, tokenizer
    if model is None:
        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained=None
        )
        model.load_state_dict(torch.load("weights/ViT-B-32.pt", map_location="cpu"))
        model.eval()
        tokenizer = open_clip.get_tokenizer("ViT-B-32")
