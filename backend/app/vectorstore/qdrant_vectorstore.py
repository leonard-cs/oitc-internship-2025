from abc import ABC, abstractmethod

from qdrant_client import QdrantClient
from qdrant_client.http.models import models


class VectorStore(ABC):
    @abstractmethod
    def create_collection(self, collection_name: str, vector_size: int) -> bool:
        pass

    @abstractmethod
    def get_collections(self) -> list[str]:
        pass

    @abstractmethod
    def get_collection_info(self) -> list[dict[str, dict[str, any]]]:
        pass


class MyQdrantVectorStore(VectorStore):
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

    def get_collections(self) -> list[str]:
        """Get list name of all existing collections

        Returns:
            List of the collections
        """
        collections_response = self.client.get_collections()
        collection_descriptions = collections_response.collections
        collection_names = [collection.name for collection in collection_descriptions]
        return collection_names

    def get_collection_info(self) -> list[dict[str, dict[str, any]]]:
        """Get list information for all existing collections

        Returns:
            List of the dictionaries with collection name and metadata
        """
        return [
            {collection: {"points": self.client.count(collection).count}}
            for collection in self.get_collections()
        ]
