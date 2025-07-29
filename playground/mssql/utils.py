import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyodbc
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("./playground/.env"))
MSSQL_SERVER = os.getenv("MSSQL_SERVER", "localhost\SQLEXPRESS")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "northwind")

EXPORT_DIR = "exports"
TIME = datetime.now().strftime("%Y%m%d_%H%M%S")


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


def delete_file(path: str, prefix: str = "", sufix: str = ""):
    for filename in os.listdir(path):
        if filename.startswith(prefix) and filename.endswith(sufix):
            os.remove(os.path.join(path, filename))
