from fastapi import APIRouter

from backend.app.config import backend_logger
from backend.app.models.vectorstore import (
    AllIdRequest,
    AllIdResponse,
    SyncRequest,
    SyncResponse,
)
from backend.app.services.vectorstore import get_all_ids, handle_sync_collection

router = APIRouter()


@router.post("/sync_collection", response_model=SyncResponse)
async def sync_collection(payload: SyncRequest) -> SyncResponse:
    handle_sync_collection(payload.collection)
    return SyncResponse(status="success", collection=payload.collection)


@router.get("/all_ids", response_model=list[AllIdResponse])
async def all_ids(payload: AllIdRequest) -> list[AllIdResponse]:
    backend_logger.info(
        f"Retrieving all IDs from collection: {payload.collection.value}"
    )
    return get_all_ids(
        collection_name=payload.collection.value, with_payload=payload.with_payload
    )
