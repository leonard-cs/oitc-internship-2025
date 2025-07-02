import pyodbc
import pandas as pd
import json
import sys
import os

from db_uploader.config import MSSQL_DRIVER, MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USERNAME, MSSQL_PASSWORD

def export_each_product_to_json(table: str, output_folder: str):
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

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Export each row as its own JSON file
        for idx, row in df.iterrows():
            product_id = row.get("ProductID") or idx  # fallback to index if no ProductID
            output_file = os.path.join(output_folder, f"Product_{product_id}.json")
            # Convert the row to dict and dump as JSON
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(row.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"📁 Exported {len(df)} products to '{output_folder}'")
    except Exception as e:
        print("❌ Error during data export:", e)
    finally:
        conn.close()
        print("🔌 Connection closed.")