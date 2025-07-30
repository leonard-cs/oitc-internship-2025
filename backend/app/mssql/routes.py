from fastapi import APIRouter, Query

from backend.app.mssql.services import fetch_table_names, fetch_table_info

router = APIRouter()


@router.get("/table-names")
async def get_table_names() -> list[str]:
    """
    Get all table names from the database.
    """
    return fetch_table_names()


@router.post("/table-info")
async def get_table_info(table_names: list[str] = Query(...)) -> str:
    """
    Get information about multiple tables.
    """
    return fetch_table_info(table_names)
