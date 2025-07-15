# llm_server/embeddings/base.py

from abc import ABC, abstractmethod

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        pass

    @abstractmethod
    def embed_image(self, image_path: str) -> list[float]:
        pass