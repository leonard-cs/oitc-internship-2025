# config.py
from dotenv import load_dotenv
import os

load_dotenv()

# MSSQL
MSSQL_DRIVER = os.getenv("MSSQL_DRIVER")
MSSQL_SERVER = os.getenv("MSSQL_SERVER")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")
MSSQL_USERNAME = os.getenv("MSSQL_USERNAME")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
EXPORT_DIR = "exports"

# AnythingLLM
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_WORKSPACE_ID = os.getenv("LLM_WORKSPACE_ID")

# Ollama
OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL")
