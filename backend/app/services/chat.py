from backend.app.config import backend_logger
from backend.app.models.chat import AgentResponse, ChatResponse, LLMResponse
from backend.app.models.query_process import QueryProcessorResponse
from backend.app.models.vectorstore import CollectionName
from backend.app.services.query_processor import process_query
from backend.app.services.rag_chain import (
    generate_answer,
    generate_answer_from_docs,
    generate_answer_from_sql,
)
from backend.app.services.vectorstore import search


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
    backend_logger.debug(llm_response)
    return ChatResponse(
        answer=llm_response.answer,
        semantic_query=semantic_query,
        sources=llm_response.sources,
    )


async def handle_chat_request_sql(user_query: str) -> ChatResponse:
    backend_logger.info("Received chat request for SQL")
    llm_response = await generate_answer_from_sql(user_query)
    return ChatResponse(
        answer=llm_response.answer,
        semantic_query=user_query,
        sources=llm_response.sources,
        tools_used=["sql"],
    )


async def handle_chat_request_agent(
    user_query: str, use_query_processor: bool = False
) -> ChatResponse:
    backend_logger.info("Received chat request for agent")

    llm_response: AgentResponse = await generate_answer(user_query)

    return ChatResponse(
        semantic_query=user_query,
        answer=llm_response.answer,
        sources=llm_response.sources,
        tools_used=llm_response.tools_used,
    )
