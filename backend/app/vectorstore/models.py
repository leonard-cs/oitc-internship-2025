from enum import Enum

from pydantic import BaseModel


class CollectionName(str, Enum):
    products = "Products"
    employees = "Employees"
    employees_photos = "Employees-photos"
    test = "Test"


class SyncRequest(BaseModel):
    collection: CollectionName


class SyncResponse(BaseModel):
    collections_synced: list[str]
    collections_failed: list[str]
