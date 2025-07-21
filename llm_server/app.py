# llm_server/app.py
# uvicorn llm_server.app:app --reload

from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from llm_server.embeddings.utils import embed_image_from_upload
from llm_server.image_search.qdrant import (
    create_collection,
    get_embedding_by_id,
    save_embedding,
    search_similar,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_collection()
    print("Qdrant connection success.")
    yield


app = FastAPI(title="Image Vector Search API", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hello from the Image Vector Search API!"}


@app.post("/embed_image/")
async def embed_image(file: UploadFile = File(...)):
    """
    Receive an image file, generate its embedding, and return the embedding.
    """
    embedding = embed_image_from_upload(file)
    return JSONResponse(content={"embedding": embedding})


@app.post("/store_image/")
async def store_image(file: UploadFile = File(...)):
    try:
        embedding = embed_image_from_upload(file)
        metadata = {"filename": file.filename}
        point_id = save_embedding(embedding, metadata)
        return {"message": f"Stored image embedding with id {point_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search_similar/")
async def search_similar_images(file: UploadFile = File(...)):
    try:
        embedding = embed_image_from_upload(file)
        results = search_similar(embedding)
        hits = []
        for hit in results:
            hits.append({"id": hit.id, "score": hit.score, "metadata": hit.payload})
        return {"results": hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_embedding/{point_id}")
async def api_get_embedding(point_id: str):
    try:
        result = get_embedding_by_id(point_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
