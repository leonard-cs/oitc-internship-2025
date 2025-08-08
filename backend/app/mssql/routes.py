import pyodbc
from app.config import backend_logger
from app.mssql.dependencies import get_db, get_mssql_pyodbc_connection
from app.mssql.models import ImageTable, Table
from app.mssql.services import (
    extract_images,
    fetch_table_info,
    fetch_table_names,
    sync_table_ai,
    sync_table_images,
)
from app.vectorstore.models import SyncResponse
from fastapi import APIRouter, Depends, Query
from langchain_community.utilities import SQLDatabase

router = APIRouter()


@router.get("/table-names")
async def get_table_names(db: SQLDatabase = Depends(get_db)) -> list[str]:
    """
    Get all table names from the database.
    """
    return fetch_table_names(db)


@router.post("/table-info")
async def get_table_info(
    tables: list[Table] = Query(...),
    db: SQLDatabase = Depends(get_db),
) -> str:
    """
    Get information about multiple tables.
    """
    table_names = [table.value for table in tables]
    return fetch_table_info(db, table_names)


@router.post(
    "/ai-sync/", summary="Sync a table from the database to the vector store by AI"
)
async def ai_sync(
    tables: list[Table] = Query(..., description="Tables to sync by ai"),
    db: SQLDatabase = Depends(get_db),
) -> SyncResponse:
    """
    Sync a table from the database to the vector store by AI.
    """
    tables_synced, tables_failed = [], []
    for table in tables:
        try:
            ids = await sync_table_ai(db, table)
            if not ids:
                tables_failed.append(table.value)
            else:
                tables_synced.append(table.value)
        except Exception as e:
            backend_logger.error(f"Error syncing table {table.value}: {e}")
            tables_failed.append(table.value)
    return SyncResponse(
        success=tables_synced,
        failed=tables_failed,
    )


@router.post(
    "/ai-sync-all/",
    summary="Sync all tables from the database to the vector store by AI",
)
async def ai_sync_all(
    db: SQLDatabase = Depends(get_db),
) -> SyncResponse:
    """
    Sync all tables from the database to the vector store by AI.
    """
    tables_synced, tables_failed = [], []
    for table in Table:
        try:
            ids = await sync_table_ai(db, table)
            if not ids:
                tables_failed.append(table.value)
            else:
                tables_synced.append(table.value)
        except Exception as e:
            backend_logger.error(f"Error syncing table {table.value}: {e}")
            tables_failed.append(table.value)
    return SyncResponse(
        success=tables_synced,
        failed=tables_failed,
    )


@router.post("/sync-images")
async def sync_images(
    tables: list[ImageTable] = Query(...),
    db_connection: pyodbc.Connection = Depends(get_mssql_pyodbc_connection),
):
    """
    Sync images from the database to the vector store by AI.
    """
    tables_synced, tables_failed = [], []
    for table in tables:
        try:
            export_dir = await extract_images(db_connection, table)
            ids = await sync_table_images(table, export_dir)
            if not ids:
                tables_failed.append(table.value)
            else:
                tables_synced.append(table.value)
        except Exception as e:
            backend_logger.error(f"Error syncing table {table.value}: {e}")
            tables_failed.append(table.value)
    return SyncResponse(
        success=tables_synced,
        failed=tables_failed,
    )
