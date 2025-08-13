from app.config import backend_logger
from app.vectorstore.service import get_all_records, get_vectorstore_info
from fastapi import APIRouter, HTTPException, Query

from app.mssql.models import Table

router = APIRouter()


@router.get(
    "/info",
    summary="Get vector store information",
    description="Retrieve comprehensive information about the vector store including collections, statistics, and configuration details.",
)
async def get_info():
    """
    Get comprehensive information about the vector store.

    This endpoint provides detailed information about the current state of the vector store,
    including available collections, their sizes, configuration parameters, and health status.

    Returns:
        dict: A dictionary containing vector store information including:
            - Available collections and their metadata
            - Storage statistics and performance metrics
            - Configuration details
            - Connection status
    """
    return await get_vectorstore_info()


@router.get(
    "/collection-ids",
    response_model=list[dict],
    summary="Get all document IDs from a vector collection",
    description="Retrieve all document IDs and optionally their payload data from a specified vector store collection for inspection and debugging purposes.",
)
async def get_collection_ids(
    table: Table = Query(..., description="Collection to retrieve IDs from"),
    with_payload: bool = Query(False, description="Include payload data for each ID"),
) -> list[dict]:
    """
    Retrieve all document IDs (and optionally payloads) from a specified vector store collection.

    This endpoint is primarily used for debugging, data inspection, and administrative tasks.
    It allows you to examine what documents are stored in a collection and optionally
    retrieve their content and metadata.

    Args:
        collection (CollectionName): The name of the collection to query.
            Must be one of the predefined collection names (products, employees, test, etc.)
        with_payload (bool, optional): Whether to include document content and metadata.
            - False (default): Returns only document IDs
            - True: Returns IDs with full document content and metadata

    Returns:
        list[dict]: A list of dictionaries.
    """
    backend_logger.info(f"Retrieving all IDs from collection: {table.value}")
    try:
        return get_all_records(
            collection_name=table.value,
            with_payload=with_payload,
        )
    except Exception as e:
        backend_logger.error(f"Error retrieving from collection '{table.value}':\n{e}")
        raise HTTPException(status_code=500, detail=str(e))
