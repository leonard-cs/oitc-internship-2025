# image_search/qdrant.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import models, Filter
import uuid

COLLECTION_NAME = "image"
VECTOR_SIZE = 512

qdrant = QdrantClient(host="localhost", port=6333)

def create_collection():
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

def save_embedding(embedding: list[float], metadata: dict) -> str:
    if not isinstance(embedding, list) or len(embedding) != VECTOR_SIZE:
        raise ValueError(f"Embedding must be a list of {VECTOR_SIZE} floats.")
    point_id = str(uuid.uuid4())
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=metadata
            )
        ],
    )
    return point_id

def get_embedding_by_id(point_id: str) -> dict:
    """
    Retrieve a stored embedding and its metadata from Qdrant using point ID.
    Returns a dict with 'vector' and 'payload'.
    """
    try:
        response = qdrant.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[point_id],
            with_payload=True,
            with_vectors=True
        )

        if not response:
            raise ValueError(f"No point found with ID: {point_id}")

        point = response[0]
        return {
            "id": point.id,
            "vector": point.vector,
            "metadata": point.payload
        }

    except Exception as e:
        raise RuntimeError(f"Error retrieving embedding: {e}")

def search_similar(embedding: list, limit: int = 5):
    result = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=limit,
        with_payload=True
    )
    return result

def get_all_ids(limit: int = 10000) -> list[str]:
    """
    Retrieve all point IDs from the Qdrant collection.
    Returns a list of IDs (as strings).
    """
    all_ids = []
    offset = None

    while True:
        scroll_result = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            with_payload=False,
            with_vectors=False,
            limit=256,
            offset=offset,
        )

        points = scroll_result[0]
        if not points:
            break

        all_ids.extend([str(point.id) for point in points])
        offset = scroll_result[1]

        if offset is None or len(all_ids) >= limit:
            break

    return all_ids

if __name__ == "__main__":
    create_collection()
    print("Qdrant collection setup complete.")
    print(get_all_ids())
