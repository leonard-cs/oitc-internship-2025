import os
from functools import lru_cache

import pymssql
from app.config import (
    MSSQL_DATABASE,
    MSSQL_HOST,
    MSSQL_PASSWORD,
    MSSQL_SERVER,
    MSSQL_SQLDATABASE_PYMSSQL_CONNECTION_STRING,
    MSSQL_USERNAME,
)
from langchain_community.utilities import SQLDatabase


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
        return SQLDatabase.from_uri(MSSQL_SQLDATABASE_PYMSSQL_CONNECTION_STRING)
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")


@lru_cache(maxsize=1)
def get_SQLDatabase():
    return SQLDatabase.from_uri(MSSQL_SQLDATABASE_PYMSSQL_CONNECTION_STRING)


@lru_cache(maxsize=1)
def get_pymssql_connection() -> pymssql.Connection:
    return pymssql.connect(
        server=f"{MSSQL_HOST}\\{MSSQL_SERVER}",
        user=MSSQL_USERNAME,
        password=MSSQL_PASSWORD,
        database=MSSQL_DATABASE,
    )
