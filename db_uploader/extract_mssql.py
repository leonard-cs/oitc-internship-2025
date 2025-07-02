import pyodbc
import pandas as pd
import json
import sys

from db_uploader.config import MSSQL_DRIVER, MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USERNAME, MSSQL_PASSWORD

def export_to_json(table: str, output_file: str):
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

        data = df.to_dict(orient="records")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"📁 Exported to '{output_file}' successfully.")
    except Exception as e:
        print("❌ Error during data export:", e)
    finally:
        conn.close()
        print("🔌 Connection closed.")