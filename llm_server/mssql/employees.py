import os
import pandas as pd
import pyodbc
import sys
from llm_server.config import MSSQL_SERVER, MSSQL_DATABASE, EXPORT_DIR
from llm_server.mssql.utils import TIME, delete_file

def export_employees_csv(table: str, df: pd.DataFrame):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    file_name = os.path.join(EXPORT_DIR, f"{table}_{TIME}.csv")
    delete_file(path=EXPORT_DIR, prefix=f"{table}_", sufix="csv")

    df_to_export = df.drop(columns=["Photo", "PhotoPath"], errors="ignore")
    df_to_export.to_csv(file_name, index=False)
    print(f"✅ Table {table} saved to {file_name} as csv")

def make_employee_sentence(row: pd.Series) -> str:
    """Generate a human-readable sentence from a employee row."""
    name = f"{row['TitleOfCourtesy']} {row['FirstName']} {row['LastName']}"
    title = row['Title']
    birth_date = pd.to_datetime(row['BirthDate']).date()
    hire_date = pd.to_datetime(row['HireDate']).date()
    city = row['City']
    country = row['Country']
    reports_to = int(row['ReportsTo']) if not pd.isna(row['ReportsTo']) else "No one"
    
    return (
        f"{name} is a {title} based in {city}, {country}. "
        f"Born on {birth_date}, hired on {hire_date}. "
        f"Reports to Employee ID {reports_to}."
    )

def export_employees_sentences(table_name: str, df: pd.DataFrame) -> None:
    """Export all employee sentences into a single file."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    
    file_name = f"{table_name}_{TIME}.txt"
    file_path = os.path.join(EXPORT_DIR, file_name)

    delete_file(path=EXPORT_DIR, prefix=f"{table_name}_", sufix="txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(make_employee_sentence(row) + "\n")

    print(f"✅ Table '{table_name}' saved to {file_path} as sentences")

def export_employee_sentence_s(table_name: str, df: pd.DataFrame) -> None:
    """Export each employee sentence into a separate file."""
    folder_path = os.path.join(EXPORT_DIR, table_name)
    os.makedirs(folder_path, exist_ok=True)

    for _, row in df.iterrows():
        file_base = f"{table_name}_{row['EmployeeID']}_{TIME}"
        file_path = os.path.join(folder_path, f"{file_base}.txt")

        delete_file(path=folder_path, prefix=f"{table_name}_{row['EmployeeID']}_")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_employee_sentence(row) + "\n")

    print(f"✅ {table_name} saved to folder '{table_name}' as individual sentences")

def export_employee_photo_s(table_name: str):
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

    cursor = conn.cursor()
    cursor.execute("SELECT EmployeeID, Photo FROM Employees")

    folder_path = os.path.join(EXPORT_DIR, f"{table_name}_photos")
    os.makedirs(folder_path, exist_ok=True)

    for emp_id, photo in cursor.fetchall():
        # Strip the OLE header (78 bytes) if present
        photo_data = photo[78:]

        filename = f"{table_name}_{emp_id}_{TIME}.jpg"
        file_path = os.path.join(folder_path, filename)

        delete_file(path=folder_path, prefix=f"{table_name}_{emp_id}_", sufix=".jpg")

        with open(file_path, "wb") as f:
            f.write(photo_data)

    conn.close()
    print("✅ All employee photos exported.")