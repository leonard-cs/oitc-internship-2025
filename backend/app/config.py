import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".env"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", default="")
WEIGHTS_DIR = os.getenv("WEIGHTS_DIR", default="weights")
