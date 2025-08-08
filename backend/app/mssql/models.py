from pydantic import BaseModel, Field


class LLMDocumentResponse(BaseModel):
    id: int = Field(
        ...,
        description="The id column of the row plus the table name, e.g., 'Product_1', 'Order_5', 'Employee_10'",
    )
    text: str = Field(..., description="Generated text describing the row")
