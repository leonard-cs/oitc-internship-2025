from app.mssql.dependencies import get_db
from app.mssql.services import fetch_table_names, fetch_table_info

db = get_db()
print(fetch_table_info(db, fetch_table_names(db)))
