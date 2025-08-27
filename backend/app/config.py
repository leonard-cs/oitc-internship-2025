import os
import sys

from dotenv import load_dotenv
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="TRACE")
backend_logger = logger.bind(name="backend")

load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="http://localhost:11434")
# OLLAMA_CHAT_MODEL = os.getenv("PHI3_MODEL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("DEEPSEEK_MODEL", default="")
# OLLAMA_CHAT_MODEL = os.getenv("GEMMA_MODEL", default="")
OLLAMA_CHAT_MODEL = os.getenv("QWEN_MODEL", default="")
WEIGHTS_DIR = os.getenv("WEIGHTS_DIR", default="weights")

# Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL", default="")
QDRANT_VECTOR_SIZE: int = int(os.getenv("QDRANT_VECTOR_SIZE", default=0))

EMBEDDING_MODEL_PATH = "weights/ViT-B-32.pt"


MSSQL_HOST = os.getenv("MSSQL_HOST", default="localhost")
MSSQL_SERVER = os.getenv("MSSQL_SERVER", default="SQLEXPRESS")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", default="northwind")
MSSQL_USERNAME = os.getenv("MSSQL_USERNAME", default="")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", default="")

# MSSQL_SQLDATABASE_PYODBC_CONNECTION_STRING = (
#     f"mssql+pyodbc://{MSSQL_HOST}\\{MSSQL_SERVER}/{MSSQL_DATABASE}"
#     "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
# )

MSSQL_SQLDATABASE_PYMSSQL_CONNECTION_STRING = f"mssql+pymssql://{MSSQL_USERNAME}:{MSSQL_PASSWORD}@{MSSQL_HOST}\\{MSSQL_SERVER}/{MSSQL_DATABASE}"

MSSQL_PYODBC_CONNECTION_STRING = (
    "DRIVER={SQL Server};"
    f"SERVER={MSSQL_HOST}\\{MSSQL_SERVER};"
    f"DATABASE={MSSQL_DATABASE};"
    "Trusted_Connection=yes;"
)
