from fastapi import FastAPI

from backend.app.routers import chat, embed, health, vectorstore

app = FastAPI()


app.include_router(health.router, prefix="/health")
app.include_router(chat.router, prefix="/chat")
app.include_router(embed.router, prefix="/embed")
app.include_router(vectorstore.router, prefix="/vectorstore")
