from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/ping", tags=["health"])
async def ping():
    """
    Simple health check endpoint.
    """
    return JSONResponse(content={"status": "ok", "message": "pong 🏓"})
