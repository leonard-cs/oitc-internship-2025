from enum import Enum

from pydantic import BaseModel


class CollectionName(str, Enum):
    products = "Products"
    employees = "Employees"
    employees_photos = "Employees-photos"
    test = "Test"


class FailedTable(BaseModel):
    table: str
    error: str


class SyncResponse(BaseModel):
    success: list[str]
    failed: list[FailedTable]
