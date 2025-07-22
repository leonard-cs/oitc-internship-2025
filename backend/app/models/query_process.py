from pydantic import BaseModel, Field


class QueryProcessorResponse(BaseModel):
    original_query: str = Field(description="The original user query")
    summary: str = Field(
        description="A concise summary of the query, capturing its essence"
    )
