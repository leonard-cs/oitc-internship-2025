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


@router.get(
    "/table-names",
    response_model=list[str],
    summary="Get All Database Table Names",
    description="Retrieve a complete list of all table names from the connected MSSQL database for schema exploration and data discovery",
)
async def get_table_names(db: SQLDatabase = Depends(get_db)) -> list[str]:
    """
    Retrieve all table names from the connected MSSQL database.

    Args:
        db (SQLDatabase): Database connection dependency that provides access to the
                         MSSQL database. Automatically injected by FastAPI.

    Returns:
        list[str]: A list of table names available in the database.
    """
    return fetch_table_names(db)


@router.post(
    "/table-info",
    response_model=str,
    summary="Get Detailed Table Schema Information",
    description="Retrieve comprehensive schema information including columns, data types, constraints, and relationships for specified database tables",
)
async def get_table_info(
    tables: list[Table] = Query(
        ..., description="List of table names to retrieve schema information for"
    ),
    db: SQLDatabase = Depends(get_db),
) -> str:
    """
    Retrieve detailed schema information for multiple specified database tables.

    This endpoint provides comprehensive table metadata including column definitions,
    data types, constraints, indexes, and relationships. It's essential for understanding
    database structure before performing queries or data analysis.

    Args:
        tables (list[Table]): List of table enum values specifying which tables
                             to retrieve information for. Must be valid table names
                             from the Table enum (e.g., Table.employees, Table.products).
        db (SQLDatabase): Database connection dependency providing access to the
                         MSSQL database. Automatically injected by FastAPI.

    Returns:
        str: Formatted string containing detailed schema information for all
             requested tables, including column definitions, data types, and constraints.
             The format is human-readable and suitable for documentation or analysis.
    """
    table_names = [table.value for table in tables]
    return fetch_table_info(db, table_names)


@router.post(
    "/ai-sync/",
    response_model=SyncResponse,
    summary="AI-Powered Table Synchronization to Vector Store",
    description="Synchronize specified database tables to the vector store using AI-powered processing for enhanced semantic search and retrieval capabilities",
)
async def ai_sync(
    tables: list[Table] = Query(
        ..., description="List of database tables to synchronize to the vector store"
    ),
    limit: int | None = Query(
        None, description="Limit the number of rows to synchronize"
    ),
    db: SQLDatabase = Depends(get_db),
) -> SyncResponse:
    """
    Synchronize specified database tables to the vector store using AI-powered processing.

    This endpoint performs intelligent synchronization of database tables to a vector store,
    enabling semantic search and retrieval capabilities. The AI processing includes:
    1. Extracting and preprocessing table data
    2. Generating semantic embeddings for each record
    3. Creating searchable vector representations
    4. Storing vectors with metadata for retrieval

    Args:
        tables (list[Table]): List of table enum values to synchronize.
                             Each table will be processed independently and
                             can succeed or fail individually.
        db (SQLDatabase): Database connection dependency providing access to
                         the source MSSQL database. Automatically injected.

    Returns:
        SyncResponse: Response object containing:
            - success (list[str]): Names of tables successfully synchronized
            - failed (list[str]): Names of tables that failed to synchronize
    """
    tables_synced, tables_failed = [], []
    for table in tables:
        try:
            ids = await sync_table_ai(db, table, limit)
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
    response_model=SyncResponse,
    summary="AI-Powered Full Database Synchronization to Vector Store",
    description="Synchronize all available database tables to the vector store using AI processing for comprehensive semantic search capabilities across the entire database",
)
async def ai_sync_all(
    db: SQLDatabase = Depends(get_db),
) -> SyncResponse:
    """
    Synchronize all available database tables to the vector store using AI-powered processing.

    This endpoint performs a comprehensive synchronization of the entire database to the
    vector store, creating a complete semantic search index across all tables.

    Args:
        db (SQLDatabase): Database connection dependency providing access to
                         the source MSSQL database. Automatically injected by FastAPI.

    Returns:
        SyncResponse: Comprehensive response object containing:
            - success (list[str]): Names of all successfully synchronized tables
            - failed (list[str]): Names of tables that failed synchronization
                                 with reasons logged separately
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


@router.post(
    "/sync-images",
    response_model=SyncResponse,
    summary="AI-Powered Image Synchronization to Vector Store",
    description="Extract and synchronize image data from database tables to the vector store using AI-powered computer vision for multimodal search capabilities",
)
async def sync_images(
    tables: list[ImageTable] = Query(
        ..., description="List of image tables to extract and synchronize"
    ),
    db_connection: pyodbc.Connection = Depends(get_mssql_pyodbc_connection),
) -> SyncResponse:
    """
    Extract and synchronize image data from database tables to the vector store using AI.

    This specialized endpoint handles image data synchronization, enabling multimodal
    search capabilities by processing images stored in database tables.

    Args:
        tables (list[ImageTable]): List of image table enum values containing
                                  image data to synchronize. Each table should
                                  contain image columns (BLOB, VARBINARY, etc.).
        db_connection (pyodbc.Connection): Direct MSSQL database connection for
                                          binary data extraction. Automatically
                                          injected by FastAPI dependency.

    Returns:
        SyncResponse: Response object containing:
            - success (list[str]): Names of image tables successfully synchronized
            - failed (list[str]): Names of tables that failed image processing
    """
    tables_synced, tables_failed = [], []
    for table in tables:
        try:
            export_dir = extract_images(db_connection, table)
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
