from fastapi import APIRouter, Depends, Query
from langchain_community.utilities import SQLDatabase

from app.mssql.dependencies import get_db
from app.mssql.services import fetch_table_info, fetch_table_names

router = APIRouter()


@router.get("/table-names")
async def get_table_names(db: SQLDatabase = Depends(get_db)) -> list[str]:
    """
    Get all table names from the database.
    """
    return fetch_table_names(db)


@router.post("/table-info")
async def get_table_info(
    table_names: list[str] = Query(...),
    db: SQLDatabase = Depends(get_db),
) -> str:
    """
    Get information about multiple tables.
    """
    return fetch_table_info(db, table_names)
