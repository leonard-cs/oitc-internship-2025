from app.agent.custom_agent_executor import CustomAgentExecutor
from app.agent.models import AgentResponse
from app.chat.models import ChatResponse
from app.config import backend_logger
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()


@router.post(
    "/ask_agent",
    response_model=ChatResponse,
    summary="Process Query through Agent RAG Pipeline",
)
async def ask_chat_agent(
    query: str = Query(..., description="The user's query"),
):
    """
    Process a user query through the agentic RAG pipeline.
    """
    backend_logger.info("Received chat request for agent")
    try:
        agent = CustomAgentExecutor()
        response: AgentResponse = agent.invoke(query=query)
        return ChatResponse(
            semantic_query=query,
            answer=response.answer,
            sources=response.sources,
            tools_used=response.tools_used,
        )
    except Exception as e:
        backend_logger.error(f"Error when invoking agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
