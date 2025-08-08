import os
from functools import lru_cache

import pyodbc
from app.config import MSSQL_CONNECTION_STRING, MSSQL_PYODBC_CONNECTION_STRING
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
        return SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")


@lru_cache(maxsize=1)
def get_mssql_pyodbc_connection() -> pyodbc.Connection:
    """Establishes a connection to the SQL Server database."""
    conn: pyodbc.Connection = pyodbc.connect(MSSQL_PYODBC_CONNECTION_STRING)
    return conn
