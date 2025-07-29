from enum import Enum

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
