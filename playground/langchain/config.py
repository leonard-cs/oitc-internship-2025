import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("/playground/.env"))

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="http://localhost:11500")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", default=11500))
PHI3 = os.getenv("PHI3", default="phi3")
NOMIC = os.getenv("NOMIC", default="nomic-embed-text")
NOMIC_VECTOR_SIZE: int = int(os.getenv("NOMIC_VECTOR_SIZE", default=768))

# Qdrant
QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", default=6334))
