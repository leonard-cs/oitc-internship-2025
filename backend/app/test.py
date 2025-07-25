import re
import uuid
from pathlib import Path
from typing import Optional

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import models

from backend.app.config import QDRANT_URL, QDRANT_VECTOR_SIZE, backend_logger
from backend.app.models.vectorstore import CollectionName
from backend.app.services.embed.clipembedder import CLIPEmbedder

qdrant = QdrantClient(url=QDRANT_URL)
embedder = CLIPEmbedder()


def setup():
    collection: str = CollectionName.test.value
    _create_collection(collection)
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=embedder,
    )
    documents = [
        Document(page_content="apple", metadata={"date": "07/24"}),
        Document(page_content="grape", metadata={"date": "07/24"}),
        Document(page_content="lion", metadata={"date": "07/24"}),
        Document(page_content="orange", metadata={"date": "07/24"}),
        Document(page_content="blue", metadata={"date": "07/24"}),
        Document(page_content="strawberry", metadata={"date": "07/24"}),
        Document(page_content="sun", metadata={"date": "07/24"}),
        Document(page_content="red hair", metadata={"date": "07/24"}),
    ]
    ids = vector_store.add_documents(documents=documents)


def search(query: str) -> list:
    collection: str = CollectionName.test.value
    if not qdrant.collection_exists(collection):
        backend_logger.error(f"Collection '{collection}' does not exist.")
        return []
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=embedder,
    )
    return vector_store.similarity_search(query=query, k=4, filter=None)


def get_all_ids(
    collection_name: str, with_payload: bool = True, limit: int = 10000
) -> list[dict[str, any]]:
    all_entries = []
    offset = None

    while True:
        scroll_result = qdrant.scroll(
            collection_name=collection_name,
            with_payload=with_payload,
            with_vectors=False,
            limit=256,
            offset=offset,
        )

        points = scroll_result[0]
        if not points:
            break

        for point in points:
            # if with_payload:
            #     entry = {
            #         "id": str(point.id),
            #         "date": point.payload["date"],
            #         "time": point.payload["time"],
            #     }
            # else:
            #     entry = {"id": str(point.id)}
            all_entries.append(point)

        offset = scroll_result[1]

        if offset is None or len(all_entries) >= limit:
            break

    return all_entries


def new_handle_sync_collection(collection_name: str):
    _create_collection(collection_name)
    EXPORT_DIR = Path(f"exports/{collection_name}")
    files = sorted(EXPORT_DIR.glob(f"{collection_name}_*.txt"))
    for file_path in files:
        backend_logger.trace(f"Storing file {file_path}")
        # TODO: Check if file_path.name already exists in the collection
        id, date, time = _extract_file_info(file_path.name, collection_name)
        with file_path.open("r", encoding="utf-8") as f:
            text = f.read()
            metadata = {
                "date": date,
                "time": time,
            }
            print(
                _store_product(
                    collection=collection_name, id=id, text=text, metadata=metadata
                )
            )
    backend_logger.info(f"Collection '{collection_name}' synced.")


def _extract_file_info(
    filename: str, collection_name: str
) -> Optional[tuple[str, str, str]]:
    pattern = r"^{}_(\d+)_(\d{{8}})_(\d{{6}})".format(re.escape(collection_name))
    match = re.search(pattern, filename)
    if match:
        id, date, time = match.groups()
        return f"{collection_name}_{id}", date, time
    return None


def _store_product(collection: str, id: str, text: str, metadata: dict):
    _create_collection(collection)
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=embedder,
    )
    ids = vector_store.add_documents(
        documents=[Document(page_content=text, metadata=metadata, id=id)],
    )
    return ids[0]


def _create_collection(collection_name: str):
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=QDRANT_VECTOR_SIZE, distance=models.Distance.COSINE
            ),
        )
        backend_logger.info(f"Collection '{collection_name}' created successfully.")
    else:
        backend_logger.info(f"Collection '{collection_name}' already exists.")


if __name__ == "__main__":
    # setup()
    name = CollectionName.products.value
    # new_handle_sync_collection(name)
    print(get_all_ids(collection_name=name))
