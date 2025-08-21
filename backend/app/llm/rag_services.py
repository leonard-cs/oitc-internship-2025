from app.config import backend_logger
from app.llm.models import CollectionDecisionResponse
from app.llm.ollama import get_ollama
from app.llm.prompts import get_collection_decision_prompt


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


# TODO: move generate_answer_with_context from chat/rag_chain.py to this file
