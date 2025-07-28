from fastapi import APIRouter

from backend.app.config import backend_logger
from backend.app.models.vectorstore import (
    AllIdRequest,
    AllIdResponse,
    CollectionName,
    StoreTextRequest,
    SyncRequest,
    SyncResponse,
)
from backend.app.services.vectorstore import (
    get_all_ids,
    handle_sync_collection,
    store_text,
)

router = APIRouter()


@router.post("/sync-all", response_model=SyncResponse, tags=["vectorstore"])
async def sync_all_collections() -> SyncResponse:
    """
    Upload all collections from the database to the vector store.

    This endpoint performs a full synchronization of multiple database tables into their corresponding vector store collections.
    It is typically used to initialize or refresh the vector index with complete data.

    Returns:
        SyncResponse: A response containing two lists:
            - `collections_synced`: List of collections that were successfully synced.
            - `collections_failed`: List of collections that failed to sync.
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

    return SyncResponse(
        collections_synced=collections_synced,
        collections_failed=collections_failed,
    )


@router.post("/sync-collection", response_model=SyncResponse, tags=["vectorstore"])
async def sync_collection(payload: SyncRequest) -> SyncResponse:
    """
    Synchronize a single collection from the database to the vector store.

    This endpoint synchronizes a specific collection from the database and uploads it to the vector store. 
    It returns a response indicating whether the synchronization was successful or if there was an error.

    Args:
        payload (SyncRequest): The request body containing the name of the collection to be synced.
            The `collection` field is validated using the CollectionName Enum to ensure that only valid collections are accepted.

    Returns:
        SyncResponse: A response containing two lists:
            - `collections_synced`: List of collections that were successfully synced.
            - `collections_failed`: List of collections that failed to sync.
    """
    collection: str = payload.collection.value
    if handle_sync_collection(collection):
        return SyncResponse(collections_synced=[collection], collections_failed=[])
    else:
        return SyncResponse(collections_synced=[], collections_failed=[collection])


@router.post("/store-text")
async def store_text_endpoint(payload: StoreTextRequest) -> str:
    return store_text(payload.text)


@router.get("/all_ids", response_model=list[AllIdResponse])
async def all_ids(payload: AllIdRequest) -> list[AllIdResponse]:
    backend_logger.info(
        f"Retrieving all IDs from collection: {payload.collection.value}"
    )
    return get_all_ids(
        collection_name=payload.collection.value, with_payload=payload.with_payload
    )
