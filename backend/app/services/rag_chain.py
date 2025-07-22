from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_ollama import ChatOllama

from backend.app.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, backend_logger
from backend.app.models.chat import LLMResponse

ollama = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
)
structured_ollama = ollama.with_structured_output(LLMResponse)

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

pipelines = (
    {"query": lambda x: x["query"], "context": lambda x: x["context"]}
    | prompt_template
    | structured_ollama
)


async def generate_answer_from_docs(query: str, docs: list[str]) -> LLMResponse:
    backend_logger.trace(f"Input variables: {prompt_template.input_variables}")
    backend_logger.trace(f"Prompt template:\n{prompt_template.format(query=query, context=docs)}")
    response = pipelines.invoke({"query": query, "context": docs})
    backend_logger.success("Generated answer from LLM successfully")
    return response
