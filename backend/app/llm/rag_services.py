from app.config import backend_logger
from app.llm.models import CollectionDecisionResponse, RAGResponse
from app.llm.ollama import get_ollama
from app.llm.prompts import get_collection_decision_prompt, get_rag_prompt


def decide_collection(query: str, tables: list[str]) -> str:
    decide_collection_prompt = get_collection_decision_prompt()
    structured_ollama = get_ollama().with_structured_output(CollectionDecisionResponse)

    pipelines = (
        {"query": lambda x: x["query"], "collections": lambda x: x["collections"]}
        | decide_collection_prompt
        | structured_ollama
    )

    collection_response: CollectionDecisionResponse = pipelines.invoke(
        {"query": query, "collections": tables}
    )
    backend_logger.trace(collection_response)
    return collection_response.collection


async def generate_answer_with_context(query: str, context: str) -> RAGResponse:
    prompt_template = get_rag_prompt()
    structured_ollama = get_ollama().with_structured_output(RAGResponse)

    pipelines = (
        {"query": lambda x: x["query"], "context": lambda x: x["context"]}
        | prompt_template
        | structured_ollama
    )

    # backend_logger.trace(
    #     f"Prompt template:\n{prompt_template.format(query=query, context=context)}"
    # )

    response: RAGResponse = pipelines.invoke({"query": query, "context": context})
    backend_logger.trace(response)

    return response


# TODO: move generate_answer_from_sql from chat/rag_chain.py to this file
