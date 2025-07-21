from fastapi import FastAPI
from backend.app.routers import health, chat

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from the Backend API!"}


app.include_router(health.router, prefix="/api/health")
app.include_router(chat.router, prefix="/api/chat")
