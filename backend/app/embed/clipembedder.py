import os

import open_clip
import torch
from langchain_core.embeddings.embeddings import Embeddings
from PIL import Image

from backend.app.config import EMBEDDING_MODEL_PATH, backend_logger


class CLIPEmbedder(Embeddings):
    def __init__(self):
        """
        Initialize the CLIPEmbedder by loading the CLIP model, preprocessing pipeline, and tokenizer.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess, self.tokenizer = self._load_model(
            EMBEDDING_MODEL_PATH
        )

    def embed_query(self, text: str) -> list[float]:
        return self._handle_encode(text)

    def embed_documents(self, texts) -> list[list[float]]:
        return [self._handle_encode(text) for text in texts]

    def _load_model(self, path: str):
        """
        Load the CLIP model, preprocessing transforms, and tokenizer.

        Args:
            path (str): Path to the model weights.

        Returns:
            tuple: model, preprocessing function, tokenizer
        """
        try:
            model, _, preprocess = open_clip.create_model_and_transforms(
                model_name="ViT-B-32", pretrained="openai"
            )
            model.load_state_dict(torch.load(path, map_location=self.device))
            model.to(self.device)
            model.eval()
            tokenizer = open_clip.get_tokenizer("ViT-B-32")
            return model, preprocess, tokenizer
        except Exception as e:
            raise RuntimeError(f"Failed to load CLIP model from {path}: {e}")

    def _handle_encode(self, input: str) -> list[float]:
        input = input.strip()

        # Split by whitespace and take the last part as the path
        possible_path = input.split()[-1]
        if possible_path.lower().endswith((".png", ".jpg", ".jpeg")):
            if not os.path.exists(possible_path):
                backend_logger.error(f"Image file not found: {possible_path}")
                return []
            return self._encode_image_path(possible_path)
        else:
            return self._encode_text(input)

    def _encode_image_path(self, image_path: str) -> list[float]:
        image = self.preprocess(Image.open(image_path)).unsqueeze(0)
        return self._encode_image(image)

    def _encode_image(self, image: Image.Image) -> list[float]:
        image = self.preprocess(image).unsqueeze(0)
        with torch.no_grad():
            embedding = self.model.encode_image(image)
            embedding /= embedding.norm(p=2, dim=-1, keepdim=True)
        return embedding.squeeze(0).cpu().tolist()

    def _encode_text(self, text: str) -> list[float]:
        tokens = self.tokenizer([text])
        with torch.no_grad():
            embedding = self.model.encode_text(tokens.to(self.device))
            embedding /= embedding.norm(p=2, dim=-1, keepdim=True)
        return embedding.squeeze(0).cpu().tolist()
