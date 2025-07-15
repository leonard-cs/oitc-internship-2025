import os
import shutil
from fastapi import File, UploadFile
from llm_server.embeddings.clip_embedder import CLIPEmbedder

embedder = CLIPEmbedder()

def embed_image_from_upload(file: UploadFile = File(...)) -> list[float]:
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    embedding = embedder.embed_image(temp_file_path)
    os.remove(temp_file_path)
    return embedding