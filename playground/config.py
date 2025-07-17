import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("playground/.env"))

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_PORT = os.getenv("OLLAMA_PORT")
PHI3 = os.getenv("PHI3")
NOMIC = os.getenv("NOMIC")
NOMIC_VECTOR_SIZE: int = int(os.getenv("NOMIC_VECTOR_SIZE"))

# Qdrant
QDRANT_PORT: int = int(os.getenv("QDRANT_PORT"))
