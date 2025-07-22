from typing import Optional

from pydantic import BaseModel


class EmbedderResponse(BaseModel):
    similarity: Optional[float] = None
    image_embedding: Optional[list[float]] = None
    text_embedding: Optional[list[float]] = None
