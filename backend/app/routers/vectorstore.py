from fastapi import APIRouter

from backend.app.config import backend_logger
from backend.app.models.vectorstore import (
    AllIdRequest,
    AllIdResponse,
    CollectionName,
    SyncRequest,
    SyncResponse,
)
from backend.app.services.vectorstore import get_all_ids, handle_sync_collection

router = APIRouter()


@router.post("/sync-all", response_model=SyncResponse, tags=["Vector Store"])
async def sync_all_collections() -> SyncResponse:
    """
    Upload all collections from the database to the vector store.

    This endpoint performs a full synchronization of multiple database tables into their corresponding vector store collections.
    It is typically used to initialize or refresh the vector index with complete data.
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


@router.post("/sync-collection", response_model=SyncResponse, tags=["Vector Store"])
async def sync_collection(payload: SyncRequest) -> SyncResponse:
    """
    Synchronize a single collection from the database to the vector store.

    This endpoint synchronizes a specific collection from the database and uploads it to the vector store.
    It returns a response indicating whether the synchronization was successful or if there was an error.
    """
    collection: str = payload.collection.value
    if handle_sync_collection(collection):
        return SyncResponse(collections_synced=[collection], collections_failed=[])
    else:
        return SyncResponse(collections_synced=[], collections_failed=[collection])


@router.get("/all_ids", response_model=list[AllIdResponse])
async def all_ids(payload: AllIdRequest) -> list[AllIdResponse]:
    backend_logger.info(
        f"Retrieving all IDs from collection: {payload.collection.value}"
    )
    return get_all_ids(
        collection_name=payload.collection.value, with_payload=payload.with_payload
    )
