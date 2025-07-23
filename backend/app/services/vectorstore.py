import re
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.http.models import models

from backend.app.config import QDRANT_URL, QDRANT_VECTOR_SIZE, backend_logger
from backend.app.models.vectorstore import CollectionName, TextEntry
from backend.app.services.embed.embedder import get_embeddings

qdrant = QdrantClient(url=QDRANT_URL)


def handle_sync_collection(collection: CollectionName):
    _create_collection(collection)
    EXPORT_DIR = Path("exports/Products")
    files = sorted(EXPORT_DIR.glob("Products_*.txt"))
    for file_path in files:
        # TODO: Check if file_path.name already exists in the collection
        id, date, time = _extract_file_info(file_path.name)
        with file_path.open("r", encoding="utf-8") as f:
            text = f.read()
            embedding: list[float] = get_embeddings(text=text).text_embedding
            # backend_logger.debug(f"Embedding size: {len(embedding)}")
            _save_embedding(
                collection,
                TextEntry(id=id, embedding=embedding, date=date, time=time, text=text),
            )


def _create_collection(collection: CollectionName):
    if not qdrant.collection_exists(collection.value):
        qdrant.create_collection(
            collection_name=collection.value,
            vectors_config=models.VectorParams(
                size=QDRANT_VECTOR_SIZE, distance=models.Distance.COSINE
            ),
        )
        backend_logger.info(f"Collection '{collection.value}' created successfully.")
    else:
        backend_logger.info(f"Collection '{collection.value}' already exists.")


def _save_embedding(collection: CollectionName, entry: TextEntry) -> str:
    if (
        not isinstance(entry.embedding, list)
        or len(entry.embedding) != QDRANT_VECTOR_SIZE
    ):
        raise ValueError(f"Embedding must be a list of {QDRANT_VECTOR_SIZE} floats.")
    qdrant.upsert(
        collection_name=collection.value,
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


def _extract_file_info(filename: str) -> Optional[tuple[str, str, str]]:
    pattern = r"Products_(\d+)_(\d{8})_(\d{6})"
    match = re.search(pattern, filename)
    if match:
        product_id, date, time = match.groups()
        return product_id, date, time
    return None


async def retrieve_relevant_documents(embedding: list[float], limit: int = 5) -> tuple[list[str], list[str]]:
    points = qdrant.search(
        collection_name="Products",
        query_vector=embedding,
        limit=limit,
        with_payload=True
    )
    docs = []
    sources = []
    for point in points:
        docs.append(point.payload["text"])
        sources.append(f"Product ID: {point.id}, Date: {point.payload['date']}, Time: {point.payload['time']}")
    return docs, sources


@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y


# Define the multiply tool
@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' and 'y'."""
    return x * y


# Define the exponentiate tool
@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the power of 'y'."""
    return x**y


@tool
def subtract(x: float, y: float) -> float:
    """Subtract 'x' from 'y'."""
    return y - x


@tool
def vector_search(query: str) -> tuple[list[str], list[str]]:
    """
    Perform a vector similarity search against a set of documents.
    Returns top 5 most relevant context documents.
    """
    docs = [
        "Product 'Chai' (ID 1) is supplied by supplier #1 under category #1. Each unit contains '10 boxes x 20 bags' and costs $18.00. There are 39 in stock, 0 on order, and the reorder level is 10. It is currently available.",
        "Product 'Chang' (ID 2) is supplied by supplier #1 under category #1. Each unit contains '24 - 12 oz bottles' and costs $19.00. There are 17 in stock, 40 on order, and the reorder level is 25. It is currently available.",
        "Product 'Aniseed Syrup' (ID 3) is supplied by supplier #1 under category #2. Each unit contains '12 - 550 ml bottles' and costs $10.00. There are 13 in stock, 70 on order, and the reorder level is 25. It is currently available.",
        "Product 'Chef Anton's Cajun Seasoning' (ID 4) is supplied by supplier #2 under category #2. Each unit contains '48 - 6 oz jars' and costs $22.00. There are 53 in stock, 0 on order, and the reorder level is 0. It is currently available.",
        "Product 'Chef Anton's Gumbo Mix' (ID 5) is supplied by supplier #2 under category #2. Each unit contains '36 boxes' and costs $21.35. There are 0 in stock, 0 on order, and the reorder level is 0. It is currently discontinued.",
    ]
    sources = [f"Product {i}" for i in range(1, 6)]
    return docs, sources


@tool
def final_answer(answer: str, tools_used: list[str]) -> str:
    """Use this tool to provide a final answer to the user.
    The answer should be in natural language as this will be provided
    to the user directly. The tools_used must include a list of tool
    names that were used within the `scratchpad`.
    """
    return {"answer": answer, "tools_used": tools_used}


tools = [final_answer, vector_search, add, multiply, exponentiate, subtract]
