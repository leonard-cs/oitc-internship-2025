from abc import ABC, abstractmethod

from qdrant_client import QdrantClient
from qdrant_client.http.models import models


class VectorStore(ABC):
    @abstractmethod
    def create_collection(self, collection_name: str, vector_size: int) -> bool:
        pass


class QdrantVectorStore(VectorStore):
    def __init__(self, url: str):
        self.url = url
        self.client = QdrantClient(url=url)

    def create_collection(self, collection_name: str, vector_size: int) -> bool:
        return self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )
