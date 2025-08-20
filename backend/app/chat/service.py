from app.chat.models import ChatResponse, LLMResponse, QueryProcessorResponse
from app.chat.query_processor import process_query
from app.chat.rag_chain import generate_answer_from_sql, generate_answer_with_context
from app.config import backend_logger
from app.mssql.models import Table
from app.utils import documents_to_string
from app.vectorstore.models import CollectionName
from app.vectorstore.service import search, search_image
from fastapi import HTTPException, UploadFile


async def handle_chat_request(
    user_query: str, use_query_processor: bool = False
) -> ChatResponse:
    backend_logger.info("Received chat request")

    semantic_query = user_query
    if use_query_processor:
        processor_response: QueryProcessorResponse = await process_query(user_query)
        semantic_query = processor_response.summary

    documents = search(semantic_query, CollectionName.products.value)
    documents_string = documents_to_string(documents)
    backend_logger.debug(documents_string)

    llm_response: LLMResponse = await generate_answer_with_context(
        query=user_query, context=documents_string
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


async def handle_chat_request_image(user_query: str, image: UploadFile) -> ChatResponse:
    if not user_query or not image:
        raise HTTPException(status_code=400, detail="User query and image are required")
    backend_logger.info("Received chat request for image")

    documents = await search_image(file=image, collection=Table.employees.value)
    backend_logger.debug(documents)

    llm_response: LLMResponse = await generate_answer_with_context(
        query=user_query, context=documents
    )
    backend_logger.debug(f"LLM response: {llm_response}")
    return ChatResponse(
        answer=llm_response.answer,
        semantic_query=user_query,
        sources=llm_response.sources,
        tools_used=["image_search"],
    )
