from functools import lru_cache
from pathlib import Path

from app.config import QDRANT_URL, QDRANT_VECTOR_SIZE, backend_logger
from app.embed.clipembedder import CLIPEmbedder
from app.embed.service import handle_image_embed
from app.vectorstore.qdrant_vectorstore import MyQdrantVectorStore
from app.vectorstore.utils import extract_file_info, generate_uuid
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import models


@lru_cache(maxsize=1)
def get_qdrant_client():
    return QdrantClient(url=QDRANT_URL)


@lru_cache(maxsize=20)
def get_qdrant_vector_store(collection_name: str):
    _create_collection(collection_name)
    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=collection_name,
        embedding=CLIPEmbedder(),
    )


@lru_cache(maxsize=1)
def get_vectorstore():
    return MyQdrantVectorStore(url=QDRANT_URL)


async def get_vectorstore_info():
    vectorstore = get_vectorstore()
    return vectorstore.get_collection_info()


def handle_sync_collection(collection: str) -> list[str] | None:
    export_path = Path(f"../exports/{collection}")
    files = sorted(export_path.glob(f"{collection}_*.txt"))

    if not files:
        backend_logger.error(f"No export files found for collection: '{collection}'")
        return

    vector_store = get_qdrant_vector_store(collection)

    documents: list[Document] = []
    ids: list[str] = []

    for file_path in files:
        id_str, date, time = extract_file_info(file_path.name)
        with file_path.open("r", encoding="utf-8") as f:
            text = f.read()
            metadata = {
                "id": id_str,
                "date": date,
                "time": time,
            }
            documents.append(Document(page_content=text, metadata=metadata))
            ids.append(generate_uuid(id_str))
    added_ids = vector_store.add_documents(
        documents=documents,
        ids=ids,
    )
    backend_logger.success(f"{collection}: {len(added_ids)} entries synced.")
    return added_ids


def handle_sync_image_collection(
    photos_collection: str, text_collection: str
) -> list[str] | None:
    image_export_path = Path(f"../exports/{photos_collection}")
    image_files = sorted(image_export_path.glob(f"{photos_collection}_*.jpg"))
    if not image_files:
        backend_logger.error(
            f"No export image files found for collection: '{photos_collection}'"
        )
        return

    text_export_path = Path(f"../exports/{text_collection}")
    text_files = sorted(text_export_path.glob(f"{text_collection}_*.txt"))
    if not text_files:
        backend_logger.error(
            f"No export text files found for collection: '{text_collection}'"
        )
        return

    if len(image_files) != len(text_files):
        backend_logger.error(
            f"Number of image files ({len(image_files)}) does not match number of text files ({len(text_files)}) for collection: '{photos_collection}'"
        )
        return

    _create_collection(photos_collection)
    vector_store = get_qdrant_vector_store(photos_collection)

    documents: list[Document] = []
    ids: list[str] = []

    for image_path, text_path in zip(image_files, text_files):
        id_str, date, time = extract_file_info(text_path.name)
        with text_path.open("r", encoding="utf-8") as f:
            text = f.read()
            metadata = {
                "id": id_str,
                "date": date,
                "time": time,
            }
            documents.append(
                Document(page_content=f"{text}\n\n{image_path}", metadata=metadata)
            )
            ids.append(generate_uuid(id_str))
    added_ids = vector_store.add_documents(
        documents=documents,
        ids=ids,
    )
    backend_logger.success(f"{photos_collection}: {len(added_ids)} entries synced.")
    return added_ids


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
    offset = None
    qdrant = QdrantClient(url=QDRANT_URL)
    if not qdrant.collection_exists(collection_name):
        raise ValueError(f"Collection '{collection_name}' does not exist.")

    while True:
        scroll_result = qdrant.scroll(
            collection_name=collection_name,
            with_payload=with_payload,
            with_vectors=False,
            limit=256,
            offset=offset,
        )

        records = scroll_result[0]
        if not records:
            break

        for record in records:
            if with_payload:
                entry = {
                    "id": str(record.id),
                    "page_content": record.payload.get("page_content", ""),
                    "metadata": record.payload.get("metadata", {}),
                }
            else:
                entry = {"id": str(record.id)}
            all_records.append(entry)

        offset = scroll_result[1]

        if offset is None or len(all_records) >= limit:
            break
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
