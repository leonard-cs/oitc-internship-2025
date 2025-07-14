#app.py

import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from image_search.image_embedding import ImageEmbedder

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from my custom FastAPI app!"}

@app.post("/embed_image/")
async def embed_image(file: UploadFile = File(...)):
    """
    Receive an image file, generate its embedding, and return the embedding.
    """
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    embedding = ImageEmbedder().embed_image(temp_file_path)
    os.remove(temp_file_path)

    return JSONResponse(content={"embedding": embedding.tolist()})