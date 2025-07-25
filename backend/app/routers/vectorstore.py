from fastapi import APIRouter

from backend.app.config import backend_logger
from backend.app.models.vectorstore import (
    AllIdRequest,
    AllIdResponse,
    StoreTextRequest,
    SyncRequest,
    SyncResponse,
)
from backend.app.services.vectorstore import (
    get_all_ids,
    handle_sync_collection,
    new_handle_sync_collection,
    store_text,
)

router = APIRouter()


@router.post("/sync_collection", response_model=SyncResponse)
async def sync_collection(payload: SyncRequest) -> SyncResponse:
    new_handle_sync_collection(payload.collection)
    return SyncResponse(status="success", collection=payload.collection)


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
