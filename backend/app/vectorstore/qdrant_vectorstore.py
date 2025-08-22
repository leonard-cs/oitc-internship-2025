import uuid
from abc import ABC, abstractmethod

from app.config import QDRANT_URL, backend_logger
from app.exceptions.errors import CollectionNotFoundError
from app.vectorstore.utils import generate_uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PayloadSchemaType, PointStruct, VectorParams


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

    def collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name)

    def create_payload_index(self, collection_name: str):
        result = self.client.create_payload_index(
            collection_name=collection_name,
            field_name="myid",
            field_schema=PayloadSchemaType.TEXT,
        )
        backend_logger.info(f"Payload index created: {result}")

    def create_collection(self, collection_name: str, vector_size: int) -> bool:
        if not self.collection_exists(collection_name):
            return self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        else:
            return True

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
            {collection: {"points": (self.client.count(collection)).count}}
            for collection in self.get_collections()
        ]

    def upload_collection(
        self,
        collection_name: str,
        vectors: list[list[float]],
        page_contents: list[str],
        metadata: list[dict[str, any]] | None = None,
        ids: list[str] | None = None,
    ) -> list[str]:
        """Upload vectors and payload to the collection.
        This method will perform automatic batching of the data.
        If you need to perform a single update, use `upsert` method.
        """
        backend_logger.info(
            f"Uploading collection {collection_name} with {len(vectors)} vectors"
        )

        if metadata is None:
            metadata = [{} for _ in range(len(page_contents))]

        payload = [
            {
                "id": m.get("source") if m else None,
                "page_content": page_content,
                "metadata": m,
            }
            for page_content, m in zip(page_contents, metadata)
        ]
        ids = ids if ids else [str(uuid.uuid4()) for _ in range(len(vectors))]
        self.create_collection(collection_name, len(vectors[0]))
        self.client.upload_collection(
            collection_name=collection_name, vectors=vectors, payload=payload, ids=ids
        )
        return ids

    def upsert(
        self,
        collection_name: str,
        vector: list[float],
        page_content: str,
        metadata: dict[str, any] | None = None,
        id: str | None = None,
    ) -> str:
        """
        Update or insert a new point into the collection.

        If point with given ID already exists - it will be overwritten.
        """
        self.create_collection(collection_name, len(vector))
        id = id if id else str(uuid.uuid4())
        self.client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=id,
                    vector=vector,
                    payload={
                        "id": metadata.get("source") if metadata else id,
                        "page_content": page_content,
                        "metadata": metadata if metadata else {},
                    },
                )
            ],
        )
        return id

    def search(self, collection_name: str, vector: list[float], limit: int = 5):
        if not self.collection_exists(collection_name):
            raise CollectionNotFoundError(collection_name)
        return self.client.search(
            collection_name=collection_name, query_vector=vector, limit=limit
        )

    def delete_collection(self, collection_name: str) -> bool:
        if not self.collection_exists(collection_name):
            raise CollectionNotFoundError(collection_name)
        return self.client.delete_collection(collection_name)


if __name__ == "__main__":
    from app.embed.service import get_text_embeddings

    vectorstore = MyQdrantVectorStore(url=QDRANT_URL)
    texts = ["Chang", "water", "beer", "wine"]
    embeddings = [get_text_embeddings(t) for t in texts]
    ids = [generate_uuid(t) for t in texts]

    vectorstore.upload_collection(
        collection_name="test", vectors=embeddings, page_contents=texts, ids=ids
    )
