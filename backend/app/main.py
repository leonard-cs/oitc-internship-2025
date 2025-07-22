from fastapi import FastAPI

from backend.app.routers import chat, embed, health

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from the Backend API!"}


app.include_router(health.router, prefix="/api/health")
app.include_router(chat.router, prefix="/api/chat")
app.include_router(embed.router, prefix="/api/embed")
