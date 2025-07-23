from fastapi import APIRouter

from backend.app.models.vectorstore import SyncRequest, SyncResponse
from backend.app.services.vectorstore import handle_sync_collection

router = APIRouter()


@router.post("/sync_collection", response_model=SyncResponse)
async def sync_collection(payload: SyncRequest) -> SyncResponse:
    handle_sync_collection(payload.collection)
    return SyncResponse(status="success", collection=payload.collection)
