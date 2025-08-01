from fastapi import APIRouter, HTTPException

from app.agent.service import handle_chat_request_agent
from app.chat.models import ChatRequest

router = APIRouter()


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
