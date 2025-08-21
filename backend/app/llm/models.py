from pydantic import BaseModel, Field


class CollectionDecisionResponse(BaseModel):
    collection: str = Field(description="The collection to search for the query.")


# TODO: move LLMResponse from chat/models.py to this file
