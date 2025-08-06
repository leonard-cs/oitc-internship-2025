from fastapi import HTTPException
from app.agent.custom_agent_executor import CustomAgentExecutor
from app.agent.models import AgentResponse
from app.chat.models import ChatResponse
from app.config import backend_logger


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


async def generate_answer(query: str) -> AgentResponse:
    agent = CustomAgentExecutor()
    try:
        response: AgentResponse = agent.invoke(query=query)
        return response
    except Exception as e:
        msg = f"Error occurred while generating answer: {e}"
        backend_logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)
