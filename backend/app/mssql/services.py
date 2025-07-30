from langchain_community.utilities import SQLDatabase
from backend.app.config import MSSQL_CONNECTION_STRING


def fetch_table_names() -> list[str]:
    db = SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
    table_list = db.get_usable_table_names()
    return list(table_list)


def fetch_table_info(table_names: list[str]) -> str:
    db = SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
    table_info = db.get_table_info(table_names)
    return table_info