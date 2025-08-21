from functools import lru_cache

from app.config import QDRANT_URL, QDRANT_VECTOR_SIZE, backend_logger
from app.embed.clipembedder import get_clip_embedder
from app.embed.service import handle_image_embed
from app.vectorstore.qdrant_vectorstore import MyQdrantVectorStore
from fastapi import HTTPException, UploadFile
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import models


@lru_cache(maxsize=1)
def get_qdrant_client():
    return QdrantClient(url=QDRANT_URL)


@lru_cache(maxsize=20)
def get_qdrant_vector_store(collection_name: str):
    try:
        return QdrantVectorStore(
            client=get_qdrant_client(),
            collection_name=collection_name,
            embedding=get_clip_embedder(),
        )
    except UnexpectedResponse as e:
        raise HTTPException(status_code=e.status_code, detail=e.content.decode("utf-8"))


@lru_cache(maxsize=1)
def get_vectorstore():
    return MyQdrantVectorStore(url=QDRANT_URL)


def get_vectorstore_info():
    vectorstore = get_vectorstore()
    return vectorstore.get_collection_info()


def search(query: str, collection: str) -> list[Document]:
    vector_store = get_qdrant_vector_store(collection)
    return vector_store.similarity_search(query=query, k=4, filter=None)


async def search_image(file: UploadFile, collection: str) -> list[Document]:
    qdrant = get_qdrant_client()
    if not qdrant.collection_exists(collection):
        backend_logger.error(f"Collection '{collection}' does not exist.")
        return []
    backend_logger.info(f"Searching for image in collection: '{collection}'")

    image_embedding = await handle_image_embed(file)
    results: list[Document] = embedding_search(image_embedding, collection)
    return results


def embedding_search(
    embedding: list, collection: str, limit: int = 1
) -> list[Document]:
    backend_logger.trace(f"Searching for embedding in collection: '{collection}'")
    qdrant = get_qdrant_client()
    points = qdrant.search(
        collection_name=collection,
        query_vector=embedding,
        limit=limit,
        with_payload=True,
    )
    documents = []
    for point in points:
        documents.append(
            Document(
                page_content=point.payload.get("page_content", ""),
                metadata=point.payload.get("metadata", {}),
            )
        )
    backend_logger.trace(f"Documents: {documents}")
    return documents


def _create_collection(collection_name: str):
    qdrant = get_qdrant_client()
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


def get_all_records(
    collection_name: str, with_payload: bool = True, limit: int = 10000
) -> list[dict[str, any]]:
    all_records = []
    qdrant = QdrantClient(url=QDRANT_URL)
    if not qdrant.collection_exists(collection_name):
        raise ValueError(f"Collection '{collection_name}' does not exist.")

    scroll_result = qdrant.scroll(
        collection_name=collection_name, with_payload=with_payload
    )

    records = scroll_result[0]
    if not records:
        raise ValueError(f"No records found in collection '{collection_name}'.")

    for record in records:
        if with_payload:
            entry = {
                "page_content": record.payload.get("page_content", ""),
                "metadata": record.payload.get("metadata", {}),
            }
        else:
            entry = {"id": str(record.id)}
        all_records.append(entry)

    backend_logger.info(f"#Records: {len(all_records)}.")
    return all_records


async def retrieve_relevant_documents(
    embedding: list[float], limit: int = 5
) -> tuple[list[str], list[str]]:
    qdrant = get_qdrant_client()
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
