from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    "/ping",
    summary="System Health Check",
    description="Quick health check endpoint to verify the API is running and responsive",
    response_description="Returns system status and uptime confirmation",
)
async def ping():
    """
    Perform a simple health check to verify API availability and responsiveness.

    Returns:
        JSONResponse: A simple response containing:
            - status (str): "ok" indicating the service is healthy
            - message (str): Friendly confirmation message with emoji

    Response Example:
        {
            "status": "ok",
            "message": "pong 🏓"
        }
    """
    return JSONResponse(content={"status": "ok", "message": "pong 🏓"})
