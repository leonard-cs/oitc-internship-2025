from functools import lru_cache

from app.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL
from langchain_ollama import ChatOllama


@lru_cache(maxsize=1)
def get_ollama() -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_CHAT_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.0,
    )


@lru_cache(maxsize=1)
def get_stream_ollama() -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_CHAT_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.0,
        stream=True,
        reasoning=False,
    )
