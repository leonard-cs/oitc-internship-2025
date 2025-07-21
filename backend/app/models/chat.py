from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    user_query: str
    use_query_processor: bool = True  # Optional toggle


class ChatResponse(BaseModel):
    answer: str
    semantic_query: str
    sources: List[str]
