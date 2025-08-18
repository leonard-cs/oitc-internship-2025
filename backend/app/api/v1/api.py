from app.agent.routes import router as agent_router
from app.chat.routes import router as chat_router
from app.embed.routes import router as embed_router
from app.health.routes import router as health_router
from app.mssql.routes import router as mssql_router
from app.vectorstore.routes import router as vectorstore_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(mssql_router, prefix="/mssql", tags=["mssql"])
api_router.include_router(embed_router, prefix="/embed", tags=["embed"])
api_router.include_router(
    vectorstore_router, prefix="/vectorstore", tags=["vectorstore"]
)
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(agent_router, prefix="/agent", tags=["agent"])
