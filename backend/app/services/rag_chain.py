from fastapi import HTTPException
from langchain_ollama import ChatOllama

from backend.app.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, backend_logger
from backend.app.models.chat import AgentResponse, LLMResponse
from backend.app.services.custom_agent_executor import CustomAgentExecutor
from backend.app.prompts.prompts import get_rag_prompt

ollama = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
)


async def generate_answer_from_docs(query: str, docs: list[str]) -> LLMResponse:
    prompt_template = get_rag_prompt()

    structured_ollama = ollama.with_structured_output(LLMResponse)

    pipelines = (
        {"query": lambda x: x["query"], "context": lambda x: x["context"]}
        | prompt_template
        | structured_ollama
    )

    backend_logger.trace(f"Input variables: {prompt_template.input_variables}")
    backend_logger.trace(
        f"Prompt template:\n{prompt_template.format(query=query, context=docs)}"
    )
    response: LLMResponse = pipelines.invoke({"query": query, "context": docs})
    backend_logger.trace(response)
    backend_logger.success("Generated answer from LLM successfully")
    return response


async def generate_answer(query: str) -> AgentResponse:
    agent = CustomAgentExecutor()
    try:
        response: AgentResponse = agent.invoke(query=query)
        return response
    except Exception as e:
        msg = f"Error occurred while generating answer: {e}"
        backend_logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)
