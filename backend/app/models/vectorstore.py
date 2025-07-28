from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CollectionName(str, Enum):
    products = "Products"
    employees = "Employees"
    test = "Test"


class SyncRequest(BaseModel):
    collection: CollectionName


class SyncResponse(BaseModel):
    collections_synced: list[str]
    collections_failed: list[str]


class AllIdRequest(BaseModel):
    collection: CollectionName
    with_payload: Optional[bool] = False


class AllIdResponse(BaseModel):
    id: str
    date: Optional[str] = None
    time: Optional[str] = None
