import os
import pandas as pd

from llm_server.config import EXPORT_DIR
from llm_server.mssql.utils import TIME, delete_file

def export_products_csv(table: str, df: pd.DataFrame):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    file_name = os.path.join(EXPORT_DIR, f"{table}_{TIME}.csv")
    delete_file(path=EXPORT_DIR, prefix=f"{table}_", sufix="csv")
    df.to_csv(file_name, index=False)
    print(f"✅ Table {table} saved to {file_name} as csv")

def make_product_sentence(row: pd.Series) -> str:
    """Generate a human-readable sentence from a product row."""
    return (
        f"Product '{row['ProductName']}' (ID {row['ProductID']}) is supplied by supplier #{row['SupplierID']} "
        f"under category #{row['CategoryID']}. Each unit contains '{row['QuantityPerUnit']}' and costs ${row['UnitPrice']:.2f}. "
        f"There are {row['UnitsInStock']} in stock, {row['UnitsOnOrder']} on order, and the reorder level is {row['ReorderLevel']}. "
        f"{'It is currently discontinued.' if row['Discontinued'] else 'It is currently available.'}"
    )

def export_products_sentences(table_name: str, df: pd.DataFrame) -> None:
    """Export all product sentences into a single file."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    
    file_name = f"{table_name}_{TIME}.txt"
    file_path = os.path.join(EXPORT_DIR, file_name)

    delete_file(path=EXPORT_DIR, prefix=f"{table_name}_", sufix="txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(make_product_sentence(row) + "\n")

    print(f"✅ Table '{table_name}' saved to {file_path} as sentences")

def export_product_sentence_s(table_name: str, df: pd.DataFrame) -> None:
    """Export each product sentence into a separate file."""
    folder_path = os.path.join(EXPORT_DIR, table_name)
    os.makedirs(folder_path, exist_ok=True)

    for _, row in df.iterrows():
        file_base = f"{table_name}_{row['ProductID']}_{TIME}"
        file_path = os.path.join(folder_path, f"{file_base}.txt")

        delete_file(path=folder_path, prefix=f"{table_name}_{row['ProductID']}_")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_product_sentence(row) + "\n")

    print(f"✅ {table_name} saved to folder '{table_name}' as individual sentences")
