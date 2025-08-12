from abc import ABC, abstractmethod

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


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
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
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

    def upload_collection(
        self,
        collection_name: str,
        vectors: list[list[float]],
        payload: list[dict[str, any]],
        ids: list[str],
    ) -> None:
        """Upload vectors and payload to the collection.
        This method will perform automatic batching of the data.
        If you need to perform a single update, use `upsert` method.
        """
        self.client.upload_collection(
            collection_name=collection_name, vectors=vectors, payload=payload, ids=ids
        )
        self.client.upsert(
            collection_name=collection_name,
            vectors=vectors,
            payload=payload,
            ids=ids,
        )

    def upsert(
        self,
        collection_name: str,
        vector: list[float],
        payload: dict[str, any],
        id: str,
    ) -> None:
        """
        Update or insert a new point into the collection.

        If point with given ID already exists - it will be overwritten.
        """
        self.client.upsert(
            collection_name=collection_name,
            points=[PointStruct(id=id, vector=vector, payload=payload)],
        )
