import re
import uuid
from pathlib import Path
from typing import Optional

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import models

from backend.app.config import QDRANT_URL, QDRANT_VECTOR_SIZE, backend_logger
from backend.app.models.vectorstore import CollectionName, TextEntry
from backend.app.services.embed.clipembedder import CLIPEmbedder
from backend.app.services.embed.embedder import get_embeddings

qdrant = QdrantClient(url=QDRANT_URL)
# embedder = CLIPEmbedder()


def store_text(text: str) -> str:
    collection: str = CollectionName.test.value
    _create_collection(collection)
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=CLIPEmbedder(),
    )
    ids = vector_store.add_documents(
        documents=[Document(page_content=text, metadata={"date": "07/24"})]
    )
    return ids[0]


def search(query: str) -> list:
    collection: str = CollectionName.test.value
    if not qdrant.collection_exists(collection):
        backend_logger.error(f"Collection '{collection}' does not exist.")
        return []
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=CLIPEmbedder(),
    )
    return vector_store.similarity_search(query=query, k=4, filter=None)


def handle_sync_collection(collection: CollectionName):
    _create_collection(collection.value)
    EXPORT_DIR = Path(f"exports/{collection.value}")
    files = sorted(EXPORT_DIR.glob(f"{collection.value}_*.txt"))
    for file_path in files:
        # TODO: Check if file_path.name already exists in the collection
        id, date, time = _extract_file_info(file_path.name, collection.value)
        with file_path.open("r", encoding="utf-8") as f:
            text = f.read()
            embedding: list[float] = get_embeddings(text=text).text_embedding
            # backend_logger.debug(f"Embedding size: {len(embedding)}")
            _save_embedding(
                collection_name=collection.value,
                entry=TextEntry(
                    id=id, embedding=embedding, date=date, time=time, text=text
                ),
            )


def new_handle_sync_collection(collection: CollectionName):
    _create_collection(collection.value)
    EXPORT_DIR = Path(f"exports/{collection.value}")
    files = sorted(EXPORT_DIR.glob(f"{collection.value}_*.txt"))
    for file_path in files:
        # TODO: Check if file_path.name already exists in the collection
        id, date, time = _extract_file_info(file_path.name, collection.value)
        with file_path.open("r", encoding="utf-8") as f:
            text = f.read()
            metadata = {
                "date": date,
                "time": time,
            }
            _store_product(
                collection=collection.value, id=id, text=text, metadata=metadata
            )


def _store_product(collection: str, id: str, text: str, metadata: dict):
    _create_collection(collection)
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=CLIPEmbedder(),
    )
    ids = vector_store.add_documents(
        documents=[Document(page_content=text, metadata=metadata, id=id)],
        ids=[str(uuid.uuid4())],
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


def _save_embedding(collection_name: str, entry: TextEntry) -> str:
    if (
        not isinstance(entry.embedding, list)
        or len(entry.embedding) != QDRANT_VECTOR_SIZE
    ):
        raise ValueError(f"Embedding must be a list of {QDRANT_VECTOR_SIZE} floats.")
    qdrant.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=int(entry.id),
                vector=entry.embedding,
                payload={"text": entry.text, "date": entry.date, "time": entry.time},
            )
        ],
    )
    # backend_logger.info(
    #     f"Saved embedding for ID: {entry.id} in collection: {collection.value}"
    # )
    return entry.id


def _extract_file_info(
    filename: str, collection_name: str
) -> Optional[tuple[str, str, str]]:
    pattern = r"^{}_(\d+)_(\d{{8}})_(\d{{6}})".format(re.escape(collection_name))
    match = re.search(pattern, filename)
    if match:
        id, date, time = match.groups()
        return f"{collection_name}_{id}", date, time
    return None


def get_all_ids(
    collection_name: str, with_payload: bool, limit: int = 10000
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
            if with_payload:
                entry = {
                    "id": str(point.id),
                    "date": point.payload["date"],
                    "time": point.payload["time"],
                }
            else:
                entry = {"id": str(point.id)}
            all_entries.append(entry)

        offset = scroll_result[1]

        if offset is None or len(all_entries) >= limit:
            break

    return all_entries


async def retrieve_relevant_documents(
    embedding: list[float], limit: int = 5
) -> tuple[list[str], list[str]]:
    points = qdrant.search(
        collection_name="Products",
        query_vector=embedding,
        limit=limit,
        with_payload=True,
    )
    docs = []
    sources = []
    for point in points:
        docs.append(point.payload["text"])
        sources.append(
            f"Product ID: {point.id}, Date: {point.payload['date']}, Time: {point.payload['time']}"
        )
    return docs, sources


@tool
def vector_search(query: str, collection_name: str) -> tuple[list[str], list[str]]:
    """
    Perform a vector similarity search against a set of documents.
    The query should contain the semantic meaning of original query.
    collection_name can be "Products" or "Employees"
    Returns top 5 most relevant context documents and their sources.
    """
    embedding = get_embeddings(text=query).text_embedding
    points = qdrant.search(
        collection_name=collection_name,
        query_vector=embedding,
        limit=5,
        with_payload=True,
    )
    docs = []
    sources = []
    for point in points:
        docs.append(point.payload["text"])
        sources.append(
            f"{collection_name} ID: {point.id}, Date: {point.payload['date']}, Time: {point.payload['time']}"
        )
    return docs, sources


@tool
def gen_embedding(text: str) -> list:
    """
    Generate an embedding of a text.
    Return embeddings
    """
    result = get_embeddings(text=text)
    return result.text_embedding


@tool
def final_answer(answer: str, sources: list[str], tools_used: list[str]) -> dict:
    """Use this tool to provide a final answer to the user.
    The answer should be in natural language as this will be provided
    to the user directly. The tools_used must include a list of tool
    names that were used within the `scratchpad`.
    """
    return {"answer": answer, "sources": sources, "tools_used": tools_used}


tools = [final_answer, vector_search]
