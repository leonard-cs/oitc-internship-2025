from fastapi import APIRouter, HTTPException, Query

from backend.app.agent.service import handle_chat_request_agent
from backend.app.chat.models import ChatRequest, ChatResponse
from backend.app.chat.service import handle_chat_request, handle_chat_request_sql

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


@router.post("/ask_agent")
async def ask_chat_agent(payload: ChatRequest):
    """
    Process a user query through the agent RAG chatbot pipeline.
    Optionally runs a query processor before retrieval.
    """
    try:
        result = await handle_chat_request_agent(
            user_query=payload.user_query,
            use_query_processor=payload.use_query_processor,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
