from backend.app.config import backend_logger
from backend.app.chat.models import ChatResponse, LLMResponse
from backend.app.chat.models import QueryProcessorResponse
from backend.app.vectorstore.models import CollectionName
from backend.app.chat.query_processor import process_query
from backend.app.chat.rag_chain import (
    generate_answer_from_docs,
    generate_answer_from_sql,
)
from backend.app.vectorstore.service import search


async def handle_chat_request(
    user_query: str, use_query_processor: bool = False
) -> ChatResponse:
    backend_logger.info("Received chat request")

    semantic_query = user_query
    if use_query_processor:
        processor_response: QueryProcessorResponse = await process_query(user_query)
        semantic_query = processor_response.summary

    documents = search(semantic_query, CollectionName.products.value)
    backend_logger.debug(documents)

    llm_response: LLMResponse = await generate_answer_from_docs(
        query=user_query, docs=documents
    )
    backend_logger.debug(f"LLM response: {llm_response}")
    return ChatResponse(
        answer=llm_response.answer,
        semantic_query=semantic_query,
        sources=llm_response.sources,
        tools_used=["vector_search"],
    )


async def handle_chat_request_sql(user_query: str) -> ChatResponse:
    backend_logger.info("Received chat request for SQL")
    llm_response: LLMResponse = await generate_answer_from_sql(user_query)
    return ChatResponse(
        answer=llm_response.answer,
        semantic_query=user_query,
        sources=llm_response.sources,
        tools_used=[{"type": "sql", "query": llm_response.log}],
    )
