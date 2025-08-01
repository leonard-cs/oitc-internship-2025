from langchain_community.utilities import SQLDatabase

from app.config import backend_logger


def fetch_table_names(db) -> list[str]:
    table_list = db.get_usable_table_names()
    backend_logger.trace(f"\nTable list: {table_list}")
    return list(table_list)


def fetch_table_info(db, table_names: list[str]) -> str:
    table_info = db.get_table_info(table_names)
    backend_logger.trace(f"Table info:\n{table_info}")
    return table_info

def execute_sql(db, sql_query: str) -> str:
    if isinstance(db, SQLDatabase):
        return db.run_no_throw(sql_query)
    return "Database connection failed"
