from fastapi import APIRouter

from app.agent.routes import router as agent_router
from app.chat.routes import router as chat_router
from app.embed.routes import router as embed_router
from app.health.routes import router as health_router
from app.mssql.routes import router as mssql_router
from app.vectorstore.routes import router as vectorstore_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(mssql_router, prefix="/mssql", tags=["MSSQL"])
api_router.include_router(embed_router, prefix="/embed", tags=["Embed"])
api_router.include_router(
    vectorstore_router, prefix="/vectorstore", tags=["Vector Store"]
)
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
api_router.include_router(agent_router, prefix="/agent", tags=["Agent"])
