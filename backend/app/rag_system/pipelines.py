from app.chat.rag_chain import generate_answer_with_context
from app.config import backend_logger
from app.llm.models import RAGResponse
from app.llm.rag_services import decide_collection
from app.mssql.models import Table
from app.utils import documents_to_string
from app.vectorstore.service import search


async def vector_rag_pipeline(query: str) -> RAGResponse:
    backend_logger.info("Deciding which collection to search...")
    collection = decide_collection(query, Table.values())

    backend_logger.info(f"Searching collection: {collection}...")
    documents = search(query, collection)
    documents_string = documents_to_string(documents)

    backend_logger.info("Generating the answer...")
    return await generate_answer_with_context(query, documents_string)
