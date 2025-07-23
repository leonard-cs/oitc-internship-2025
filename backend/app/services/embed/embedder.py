import io

import open_clip
import torch
from PIL import Image

from backend.app.config import backend_logger
from backend.app.models.embed import EmbedderResponse

model = None
preprocess = None
tokenizer = None


def load_model():
    global model, preprocess, tokenizer
    if model is None:
        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained=None
        )
        model.load_state_dict(torch.load("weights/ViT-B-32.pt", map_location="cpu"))
        model.eval()
        tokenizer = open_clip.get_tokenizer("ViT-B-32")


@torch.no_grad()
def get_embeddings(image_bytes: bytes = None, text: str = None) -> EmbedderResponse:
    load_model()
    image_features = None
    text_features = None
    similarity = None

    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_tensor = preprocess(image).unsqueeze(0)
        image_features = model.encode_image(image_tensor)
        image_features /= image_features.norm(dim=-1, keepdim=True)

    if text:
        text_tokens = tokenizer([text])
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    if image_features is not None and text_features is not None:
        similarity = (image_features @ text_features.T).item()

    # if image_features is None and text_features is None:
    #     backend_logger.warning("Both image and text are missing")
    # else:
    #     backend_logger.success("Generated embeddings successfully")
    return EmbedderResponse(
        similarity=similarity,
        image_embedding=image_features[0].tolist()
        if image_features is not None
        else [float()],
        text_embedding=text_features[0].tolist()
        if text_features is not None
        else [float()],
    )
