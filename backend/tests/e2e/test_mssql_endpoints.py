import os

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import backend_logger
from app.mssql.routes import get_db, router

app = FastAPI()
app.include_router(router)


class MockSQLDatabase:
    def get_usable_table_names(self):
        return ["mock_table1", "mock_table2"]

    def get_table_info(self, tables):
        return f"Fake info for: {', '.join(tables)}"


# app.dependency_overrides[get_db] = lambda: MockSQLDatabase()

client = TestClient(app)


def test_get_table_names():
    backend_logger.info(f"APP_ENV: {os.getenv('APP_ENV')}")
    response = client.get("/table-names")
    assert response.status_code == 200
    # assert response.json() == ["mock_table1", "mock_table2"]


def test_get_table_info():
    response = client.post("/table-info", params=[("tables", "Products")])
    assert response.status_code == 200
    # assert response.json() == "Fake info for: mock_table1"
