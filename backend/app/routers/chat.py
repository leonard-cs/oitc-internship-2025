from fastapi import APIRouter, HTTPException
from backend.app.models.chat import ChatRequest, ChatResponse
from backend.app.services.chat import handle_chat_request

router = APIRouter()


@router.post("/ask", response_model=ChatResponse, tags=["chat"])
async def ask_chat(payload: ChatRequest) -> ChatResponse:
    """
    Process a user query through the full RAG chatbot pipeline.
    Optionally runs a query processor before retrieval.
    """
    try:
        result = await handle_chat_request(
            user_query=payload.user_query,
            use_query_processor=payload.use_query_processor,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
