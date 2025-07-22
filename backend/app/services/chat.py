from backend.app.config import backend_logger
from backend.app.models.chat import ChatResponse, LLMResponse
from backend.app.models.query_process import QueryProcessorResponse
from backend.app.services.embed.embedder import get_embeddings
from backend.app.services.query_processor import process_query
from backend.app.services.rag_chain import generate_answer_from_docs
from backend.app.services.vectorstore import retrieve_relevant_documents


async def handle_chat_request(
    user_query: str, use_query_processor: bool = True
) -> ChatResponse:
    backend_logger.info("Received chat request")

    semantic_query = user_query
    if use_query_processor:
        processor_response: QueryProcessorResponse = await process_query(user_query)
        semantic_query = processor_response.summary
    query_embedding: list[float] = get_embeddings(text=semantic_query).text_embedding

    # TODO: retrieve relevant documents
    docs, sources = await retrieve_relevant_documents(query_embedding)
    llm_response: LLMResponse = await generate_answer_from_docs(
        query=user_query, docs=docs
    )

    return ChatResponse(
        answer=llm_response.answer,
        semantic_query=semantic_query,
        sources=sources,
    )
