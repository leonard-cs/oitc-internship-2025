from app.agent.service import handle_chat_request_agent
from app.chat.models import ChatResponse
from fastapi import APIRouter, Query

router = APIRouter()


@router.post(
    "/ask_agent",
    response_model=ChatResponse,
    summary="Process Query through Agent RAG Pipeline",
    description="Process user queries through an intelligent agent-based Retrieval-Augmented Generation system with tool utilization capabilities",
)
async def ask_chat_agent(
    query: str = Query(
        ..., description="The user's question, request, or conversation input"
    ),
):
    """
    Process a user query through the intelligent agent RAG chatbot pipeline.

    Args:
        payload (ChatRequest): The chat request containing:
            - user_query (str): The user's question, request, or conversation input
            - use_query_processor (bool, optional): disabled for agent

    Returns:
        ChatResponse: The processed response containing:
            - semantic_query (str): The processed/semantic version of the query
            - answer (str): Comprehensive response utilizing agent capabilities
            - sources (list[str]): List of source document references used
            - tools_used (list, optional): Tools and reasoning chains utilized
    """
    return await handle_chat_request_agent(user_query=query)
