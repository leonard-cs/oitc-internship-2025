from app.mssql.models import Table
from app.mssql.services import fetch_table_info
from app.mssql.utils import extract_sql_results, remove_sample_rows
from langchain_community.utilities import SQLDatabase

MSSQL_CONNECTION_STRING = (
    "mssql+pyodbc://AMRO\\SQLEXPRESS/northwind"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)


def get_table_schema_demo(db: SQLDatabase):
    table_schema = fetch_table_info(db, [Table.products.value])
    print(table_schema)

    table_schema = remove_sample_rows(table_schema)
    print(table_schema)


def execute_sql_demo(db: SQLDatabase):
    result = db.run(Table.categories.sql())
    # print(result)
    rows = extract_sql_results(result)
    for row in rows:
        print(row)


def main():
    db = SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
    # get_table_schema_demo(db)
    execute_sql_demo(db)


# uv run python -m app.mssql.example
if __name__ == "__main__":
    main()
