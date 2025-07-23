from enum import Enum

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
