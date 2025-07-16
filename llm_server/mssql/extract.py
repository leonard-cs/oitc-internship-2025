import pyodbc
import pandas as pd
from pathlib import Path

from llm_server.config import MSSQL_SERVER, MSSQL_DATABASE
from llm_server.mssql.products import *
from llm_server.mssql.employees import *

def connect_to_mssql() -> pyodbc.Connection:
    """Establishes a connection to the SQL Server database."""
    conn_str: str = (
        "DRIVER={SQL Server};"
        f"SERVER={MSSQL_SERVER};"
        f"DATABASE={MSSQL_DATABASE};"
        "Trusted_Connection=yes;"
    )
    try:
        conn: pyodbc.Connection = pyodbc.connect(conn_str)
        print("✅ Connected to database.")
        return conn
    except pyodbc.Error as err:
        print("❌ Connection failed:", err)
        exit(1)

def extract_table(table: str) -> pd.DataFrame:
    conn: pyodbc.Connection = connect_to_mssql()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

def delete_file(path: str, prefix: str, sufix: str= ""):
    current_dir = Path(path)
    for file in current_dir.iterdir():
        if file.is_file() and file.name.startswith(prefix) and file.name.endswith(sufix):
            file.unlink()

if __name__ == "__main__":
    table = "Products"
    table_df = extract_table(table)
    export_products_csv(table, table_df)
    export_products_sentences(table, table_df)
    export_product_sentence_s(table, table_df)

    table = "Employees"
    table_df = extract_table(table)
    export_employees_csv(table, table_df)
    export_employees_sentences(table, table_df)
    export_employee_sentence_s(table, table_df)
    export_employee_photo_s(table)
