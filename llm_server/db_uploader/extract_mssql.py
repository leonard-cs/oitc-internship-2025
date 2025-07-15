# db_uploader/extract_mssql.py
from typing import Callable
import pyodbc
import pandas as pd
import json
import sys
import os

from config import MSSQL_DRIVER, MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USERNAME, MSSQL_PASSWORD
from db_uploader.utils import *

def connect_and_fetch(table: str) -> pd.DataFrame:
    # conn_str = f"""
    #     DRIVER={{{MSSQL_DRIVER}}};
    #     SERVER={MSSQL_SERVER};
    #     DATABASE={MSSQL_DATABASE};
    #     uid={MSSQL_USERNAME};
    #     password{MSSQL_PASSWORD}
    # """

    conn_str = (
        "DRIVER={SQL Server};"
        f"SERVER={MSSQL_SERVER};"
        f"DATABASE={MSSQL_DATABASE};"
        "Trusted_Connection=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        print("✅ Connected to database.")
    except pyodbc.Error as err:
        print("❌ Connection failed:", err)
        sys.exit(1)

    try:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        if df.empty:
            print(f"⚠️ Table '{table}' is empty.")
        else:
            print(f"✅ Retrieved {len(df)} rows from '{table}'.")
        return df
    except Exception as e:
        print("❌ Error during data export:", e)
        sys.exit(1)
    finally:
        conn.close()
        print("🔌 Connection closed.")


def export_rows(
    df: pd.DataFrame,
    output_folder: str,
    file_ext: str,
    serialize_func: Callable[[dict], str]
):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for idx, row in df.iterrows():
        product_id = row.get("ProductID") or idx
        output_file = os.path.join(output_folder, f"Product_{product_id}.{file_ext}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(serialize_func(row.to_dict()))

    print(f"📁 Exported {len(df)} products to '{output_folder}' as .{file_ext} files")

def export_each_product_to_json(table: str, output_folder: str):
    df = connect_and_fetch(table)
    export_rows(df, output_folder, "json", lambda data: json.dumps(data, ensure_ascii=False, indent=2))

def to_txt(data: dict) -> str:
    return ", ".join(f"{k}: {v}" for k, v in data.items())

def export_each_product_to_txt(table: str, output_folder: str):
    df = connect_and_fetch(table)
    export_rows(df, output_folder, "txt", to_txt)

def export_product_with_discontinued_and_stock(table: str, output_folder: str):
    df = connect_and_fetch(table)

    try:
        # Select only the two columns for export
        selected_df = df[["ProductID", "ProductName", "Discontinued", "UnitsInStock"]]
    except KeyError as e:
        print(f"❌ Missing expected column: {e}")
        return

    export_rows(selected_df, output_folder, "txt", to_txt)

def export_sentence(table: str, output_folder: str):
    df = connect_and_fetch(table)
    export_rows(df, output_folder, "txt", product_info_to_sentence)

def export_all_products_as_sentences(table: str, output_dir: str):
    df = connect_and_fetch(table)
    
    # Convert each row to a sentence
    sentences = [product_info_to_sentence(row.to_dict()) for _, row in df.iterrows()]

    # output_dir is folder, define output file name explicitly
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{table}.txt")

    with open(output_file_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")

    print(f"📝 Exported {len(sentences)} product descriptions to '{output_file_path}'")