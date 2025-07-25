import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="TRACE")
backend_logger = logger.bind(name="backend")

env_file = Path(".env")
if not env_file.is_file():
    backend_logger.error(
        f".env file not found at {env_file.resolve()}. Please make sure it exists."
    )
    sys.exit(1)

load_dotenv(dotenv_path=env_file)

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
