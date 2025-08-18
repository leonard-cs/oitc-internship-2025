from app.agent.custom_agent_executor import CustomAgentExecutor
from app.agent.models import AgentResponse
from app.chat.models import ChatResponse


async def handle_chat_request_agent(user_query: str) -> ChatResponse:
    agent = CustomAgentExecutor()
    response: AgentResponse = agent.invoke(query=user_query)
    return ChatResponse(
        semantic_query=user_query,
        answer=response.answer,
        sources=response.sources,
        tools_used=response.tools_used,
    )
