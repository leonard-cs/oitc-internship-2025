from fastapi import APIRouter, Query

from backend.app.config import backend_logger
from backend.app.vectorstore.models import (
    CollectionName,
    SyncRequest,
    SyncResponse,
)
from backend.app.vectorstore.service import get_all_records, handle_sync_collection

router = APIRouter()


@router.post("/sync-all", response_model=SyncResponse)
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


@router.post("/sync-collection", response_model=SyncResponse)
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


@router.get(
    "/collection-ids",
    response_model=list[dict],
    tags=["Vector Store"],
    summary="Get all IDs from a vector collection",
)
async def get_collection_ids(
    collection: CollectionName = Query(
        ..., description="Collection to retrieve IDs from"
    ),
    with_payload: bool = Query(False, description="Include payload data for each ID"),
) -> list[dict]:
    """
    Retrieve all IDs (and optionally payloads) from a specified vector store collection.
    """
    backend_logger.info(f"Retrieving all IDs from collection: {collection.value}")
    return get_all_records(
        collection_name=collection.value,
        with_payload=with_payload,
    )
