# llm_server/embeddings/clip_embedder.py

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from llm_server.embeddings.base import BaseEmbedder

class CLIPEmbedder(BaseEmbedder):
# class CLIPEmbedder():
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def embed_text(self, text: str) -> list[float]:
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)
        with torch.no_grad():
            features = self.model.get_text_features(**inputs)
        return self._normalize(features)

    def embed_image(self, image_path: str) -> list[float]:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
        return self._normalize(features)

    def _normalize(self, tensor: torch.Tensor) -> list[float]:
        normalized = tensor / tensor.norm(p=2, dim=-1, keepdim=True)
        return normalized.squeeze(0).cpu().tolist()

if __name__ == "__main__":
    image_path = r"C:\Users\35521\Pictures\aventador.jpg"
    print(CLIPEmbedder().embed_image(image_path))