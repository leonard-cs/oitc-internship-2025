import os
from functools import lru_cache

from langchain_community.utilities import SQLDatabase

from app.config import MSSQL_CONNECTION_STRING


class MockSQLDatabase:
    def get_usable_table_names(self):
        return {"mock_table1", "mock_table2"}

    def get_table_info(self, tables):
        return f"Fake info for: {', '.join(tables)}"


@lru_cache(maxsize=1)
def get_db():
    if os.getenv("APP_ENV") == "ci":
        return MockSQLDatabase()
    try:
        return SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")
