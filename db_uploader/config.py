from dotenv import load_dotenv
import os

load_dotenv()

MSSQL_DRIVER = os.getenv("MSSQL_DRIVER")
MSSQL_SERVER = os.getenv("MSSQL_SERVER")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")
MSSQL_USERNAME = os.getenv("MSSQL_USERNAME")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_WORKSPACE_ID = os.getenv("LLM_WORKSPACE_ID")
