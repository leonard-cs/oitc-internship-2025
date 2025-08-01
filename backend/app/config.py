import os
import sys
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="TRACE")
backend_logger = logger.bind(name="backend")

env_path = Path(".env")
if os.path.exists(env_path):
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=env_path)
else:
    backend_logger.error(f".env file not found at {os.path.abspath(env_path)}.")

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("PHI3_MODEL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("DEEPSEEK_MODEL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("GEMMA_MODEL", default="")
OLLAMA_CHAT_MODEL = os.getenv("QWEN_MODEL", default="")
WEIGHTS_DIR = os.getenv("WEIGHTS_DIR", default="weights")

# Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL", default="")
QDRANT_VECTOR_SIZE: int = int(os.getenv("QDRANT_VECTOR_SIZE", default=0))

EMBEDDING_MODEL_PATH = "weights/ViT-B-32.pt"

MSSQL_CONNECTION_STRING = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/northwind"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)
