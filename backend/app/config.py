import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path=Path(".env"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("PHI3_MODEL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("DEEPSEEK_MODEL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("GEMMA_MODEL", default="")
OLLAMA_CHAT_MODEL = os.getenv("QWEN_MODEL", default="")
WEIGHTS_DIR = os.getenv("WEIGHTS_DIR", default="weights")

logger.remove()
logger.add(sys.stderr, level="TRACE")
backend_logger = logger.bind(name="backend")
