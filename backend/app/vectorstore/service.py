from pathlib import Path

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import models

from backend.app.agent.models import AgentResponse
from backend.app.config import QDRANT_URL, QDRANT_VECTOR_SIZE, backend_logger
from backend.app.embed.clipembedder import CLIPEmbedder
from backend.app.embed.service import get_embeddings
from backend.app.vectorstore.utils import extract_file_info, generate_uuid

qdrant = QdrantClient(url=QDRANT_URL)


def handle_sync_collection(collection: str) -> list[str] | None:
    export_path = Path(f"exports/{collection}")
    files = sorted(export_path.glob(f"{collection}_*.txt"))

    if not files:
        backend_logger.error(f"No export files found for collection: '{collection}'")
        return

    _create_collection(collection)
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=CLIPEmbedder(),
    )

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


def search(query: str, collection: str) -> list[Document]:
    if not qdrant.collection_exists(collection):
        backend_logger.error(f"Collection '{collection}' does not exist.")
        return []
    vector_store = QdrantVectorStore(
        client=qdrant,
        collection_name=collection,
        embedding=CLIPEmbedder(),
    )
    return vector_store.similarity_search(query=query, k=4, filter=None)


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


def get_all_records(
    collection_name: str, with_payload: bool = True, limit: int = 10000
) -> list[dict[str, any]]:
    all_records = []
    offset = None
    qdrant = QdrantClient(url=QDRANT_URL)
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
                    "payload": record.payload.get("page_content", ""),
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
def vector_search(query: str, collection_name: str) -> list[Document]:
    """
    Perform a vector similarity search against a set of documents.
    The query should contain the semantic meaning of original query.
    collection_name can be "Products" or "Employees"
    Returns top 5 most relevant context documents and their sources.
    """
    backend_logger.info("Executing 'vector_search' tool")
    documents: list[Document] = search(query, collection_name)
    return documents


@tool
def gen_embedding(text: str) -> list:
    """
    Generate an embedding of a text.
    Return embeddings
    """
    result = get_embeddings(text=text)
    return result.text_embedding


@tool
def final_answer(answer: str, sources: list[str], tools_used: list[str]):
    """Use this tool to provide a final answer to the user.
    The answer should be in natural language as this will be provided
    to the user directly. The tools_used must include a list of tool
    names that were used within the `scratchpad`.
    """
    return AgentResponse(answer=answer, sources=sources, tools_used=tools_used)


tools = [final_answer, vector_search]
