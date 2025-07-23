from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CollectionName(str, Enum):
    products = "Products"
    employees = "Employees"


class SyncRequest(BaseModel):
    collection: CollectionName


class SyncResponse(BaseModel):
    status: str
    collection: CollectionName


class TextEntry(BaseModel):
    id: str
    embedding: list[float]
    date: str
    time: str
    text: str


class AllIdRequest(BaseModel):
    collection: CollectionName
    with_payload: Optional[bool] = False


class AllIdResponse(BaseModel):
    id: str
    date: Optional[str] = None
    time: Optional[str] = None
