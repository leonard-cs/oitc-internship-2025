from app.config import backend_logger
from app.vectorstore.models import (
    CollectionName,
    SyncRequest,
    SyncResponse,
)
from app.vectorstore.service import (
    get_all_records,
    get_vectorstore_info,
    handle_sync_collection,
    handle_sync_image_collection,
)
from fastapi import APIRouter, HTTPException, Query

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


@router.post(
    "/sync-all",
    response_model=SyncResponse,
    summary="Synchronize all collections to vector store",
    description="Perform a complete synchronization of all database collections to their corresponding vector store collections, including both text and image data.",
)
async def sync_all_collections() -> SyncResponse:
    """
    Upload all collections from the database to the vector store.

    This endpoint performs a comprehensive synchronization of multiple database tables
    into their corresponding vector store collections. It handles both text-based
    collections (products, employees, test) and image collections (employee photos).

    The synchronization process:
    1. Reads export files from the ../exports/ directory
    2. Creates vector embeddings for each document/image
    3. Stores the embeddings in Qdrant vector database
    4. Returns a summary of successful and failed synchronizations

    This operation is typically used to:
    - Initialize the vector store with complete data
    - Refresh the vector index after bulk data changes
    - Recover from vector store corruption or data loss

    Returns:
        SyncResponse: A response object containing:
            - success: List of successfully synchronized collections
            - failed: List of collections that failed to synchronize

    Raises:
        HTTPException: If there are issues accessing export files or vector store

    Note:
        This operation can take several minutes depending on the amount of data.
        Ensure export files are present in the ../exports/ directory before calling.
    """
    collections_to_sync: list[str] = [
        CollectionName.products.value,
        CollectionName.employees.value,
        CollectionName.test.value,
    ]

    collections_synced, collections_failed = [], []

    for collection in collections_to_sync:
        if handle_sync_collection(collection):
            collections_synced.append(collection)
        else:
            collections_failed.append(collection)

    image_collections: list[tuple[str, str]] = [
        (CollectionName.employees_photos.value, CollectionName.employees.value),
    ]

    for photos_collection, text_collection in image_collections:
        if handle_sync_image_collection(photos_collection, text_collection):
            collections_synced.append(photos_collection)

    return SyncResponse(
        success=collections_synced,
        failed=collections_failed,
    )


@router.post(
    "/sync-collection",
    response_model=SyncResponse,
    summary="Synchronize a specific collection to vector store",
    description="Synchronize a single specified collection from the database to the vector store with selective control over which data to sync.",
)
async def sync_collection(payload: SyncRequest) -> SyncResponse:
    """
    Synchronize a single collection from the database to the vector store.

    This endpoint provides granular control over vector store synchronization by allowing
    you to sync individual collections rather than all collections at once. This is useful
    for targeted updates, testing, or when only specific data has changed.

    The synchronization process for a single collection:
    1. Validates the specified collection exists
    2. Reads corresponding export files from ../exports/{collection}/
    3. Processes documents and creates vector embeddings
    4. Updates the vector store with new embeddings
    5. Reports success or failure status

    Args:
        payload (SyncRequest): Request body containing:
            - collection: The specific collection name to synchronize

    Returns:
        SyncResponse: A response object containing:
            - success: List containing the collection name if sync succeeded
            - failed: List containing the collection name if sync failed
    """
    collection: str = payload.collection.value
    if handle_sync_collection(collection):
        return SyncResponse(success=[collection], failed=[])
    else:
        return SyncResponse(success=[], failed=[collection])


@router.get(
    "/collection-ids",
    response_model=list[dict],
    summary="Get all document IDs from a vector collection",
    description="Retrieve all document IDs and optionally their payload data from a specified vector store collection for inspection and debugging purposes.",
)
async def get_collection_ids(
    collection: CollectionName = Query(
        ..., description="Collection to retrieve IDs from"
    ),
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
    backend_logger.info(f"Retrieving all IDs from collection: {collection.value}")
    try:
        return get_all_records(
            collection_name=collection.value,
            with_payload=with_payload,
        )
    except Exception as e:
        backend_logger.error(f"Error retrieving all IDs from collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))
