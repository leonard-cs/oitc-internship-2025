import json

from fastapi import HTTPException
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_ollama import ChatOllama

from backend.app.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, backend_logger
from backend.app.models.chat import LLMResponse
from backend.app.services.custom_agent_executor import CustomAgentExecutor

ollama = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
)


async def generate_answer_from_docs(query: str, docs: list[str]) -> LLMResponse:
    system_prompt = """You are a helpful assistant that answers questions based on the provided context.
    Your responses should be concise and directly address the user's query.
    If the context does not contain enough information to answer the question, respond with "I don't know."

    Context: 
    {context}
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )

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
    response = pipelines.invoke({"query": query, "context": docs})
    backend_logger.success("Generated answer from LLM successfully")
    return response


async def generate_answer(query: str) -> LLMResponse:
    agent = CustomAgentExecutor()
    try:
        response: str = agent.invoke(query=query)
        backend_logger.trace(f"LLM response: {response}")
        backend_logger.success("Generated answer from LLM successfully")
        response_dict = json.loads(response)
        return LLMResponse(**response_dict)
    except Exception as e:
        msg = f"Error occurred while generating answer: {e}"
        backend_logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)
