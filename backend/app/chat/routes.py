from app.chat.models import ChatRequest, ChatResponse
from app.chat.service import (
    handle_chat_request,
    handle_chat_request_image,
    handle_chat_request_sql,
)
from app.config import backend_logger
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

router = APIRouter()


@router.post("/ask", response_model=ChatResponse)
async def ask_chat(payload: ChatRequest) -> ChatResponse:
    """
    Process a user query through the full RAG chatbot pipeline.
    Optionally runs a query processor before retrieval.
    """
    try:
        result: ChatResponse = await handle_chat_request(
            user_query=payload.user_query,
            use_query_processor=payload.use_query_processor,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask-sql", response_model=ChatResponse)
async def ask_chat_sql(
    query: str = Query(..., description="User query"),
) -> ChatResponse:
    """
    Process a user query through the SQL RAG chatbot pipeline.
    """
    try:
        result: ChatResponse = await handle_chat_request_sql(user_query=query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image-query", response_model=ChatResponse)
async def process_image_query(
    file: UploadFile = File(...), user_query: str = Form(...)
) -> ChatResponse:
    """
    Process a user query through the image RAG pipeline.
    """
    backend_logger.info(
        f"Image query requested with file={file.filename}, user query={user_query}"
    )
    try:
        result: ChatResponse = await handle_chat_request_image(
            user_query=user_query, image=file
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
