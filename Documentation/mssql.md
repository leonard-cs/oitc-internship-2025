# Microsoft SQL Database

The MSSQL module provides comprehensive database integration capabilities, including schema exploration, AI-powered data synchronization to vector stores, and multimodal image processing. It serves as the primary data layer for the application's RAG (Retrieval-Augmented Generation) system.

**Module Location:** `backend/app/mssql/`

## Table of Contents
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Models](#models)
- [API Usage Examples](#api-usage-examples)
- [Services](#services)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Integration Points](#integration-points)
- [Reference](#reference)

## Key Features

### 🧠 **AI-Powered Processing**
- LLM-generated descriptions for database rows
- Structured output with Pydantic models
- Context-aware text generation using table schemas

### 🖼️ **Multimodal Support**
- Image extraction from binary database fields
- CLIP-based image embeddings
- Combined text-image vector storage

## Architecture

The MSSQL module follows a layered architecture pattern:

```
┌─────────────────┐
│   Routes        │ ← FastAPI endpoints
├─────────────────┤
│   Services      │ ← Business logic & AI processing
├─────────────────┤
│   Models        │ ← Data models & enums
├─────────────────┤
│   Dependencies  │ ← Connection management
└─────────────────┘
```

## Models

### Table Enumeration

The Table enum defines all available database tables and sql query for data extraction.

**Key Features:**
- **Predefined Table Names:** Each enum value corresponds to a specific table name in the database.
- **Customizable Queries:** SQL queries can be manually defined for each table, with optional row limiting.
- **Join Operations:** Some tables may include joins with related tables (e.g., Products ↔ Categories).

### Image Table Support

```python
class ImageTable(str, Enum):
    employees = "Employees"
    categories = "Categories"
    
    def sql_image(self, limit: int | None = None) -> str:
        # Returns queries for image extraction
```

### Response Models

```python
class LLMDocumentResponse(BaseModel):
    id: int | str = Field(..., description="Row ID with table prefix")
    text: str = Field(..., description="AI-generated descriptive text")
```

## API Usage Examples

```bash
# Get all table names
curl -X GET "http://localhost:8000/mssql/table-names"

# Get schema for specific tables
curl -X POST "http://localhost:8000/mssql/table-info" \
  -H "Content-Type: application/json" \
  -d '{"tables": ["products", "categories"]}'

# Synchronize products table
curl -X POST "http://localhost:8000/mssql/ai-sync/?tables=products&limit=50"

# Synchronize all tables
curl -X POST "http://localhost:8000/mssql/ai-sync-all/?limit=100"

# Process employee images
curl -X POST "http://localhost:8000/mssql/sync-images" \
  -H "Content-Type: application/json" \
  -d '{"tables": ["employees"]}'
```

## Services

### Table Operations
```python
def fetch_table_names(db: SQLDatabase) -> list[str]:
    """Get all usable table names from database"""

def fetch_table_info(db: SQLDatabase, table_names: list[str]) -> str:
    """Retrieve comprehensive table schema information"""
```

### AI-Powered Synchronization
```python
async def sync_table_ai(db: SQLDatabase, table: Table, limit: int | None = None) -> list[str]:
    """Synchronize table data to vector store with AI processing"""
```

**Processing Pipeline:**
1. **Data Extraction**: Execute optimized SQL queries
2. **AI Processing**: Generate descriptive text using LLM
3. **Embedding Generation**: Create vector embeddings
4. **Vector Storage**: Upload to Qdrant with metadata

### Image Processing
```python
def extract_images(db_connection: pymssql.Connection, table: ImageTable, export_dir: str = "exports") -> str:
    """Extract images from database and save to filesystem"""

async def sync_table_images(db_connection: pymssql.Connection, db: SQLDatabase, image_table: ImageTable) -> list[str]:
    """Process and synchronize image data to vector store"""
```

### Data Processing Utilities

```python
def remove_sample_rows(table_info: str) -> str:
    """Remove sample rows from the table info"""

def extract_sql_results(result_string: str) -> list[str]:
    """Parse SQL result strings into structured data"""

async def generate_text_and_id(table_name: str, row: str, table_info: str) -> tuple[str, str] | None:
    """Generate AI-powered descriptions for database rows"""
```

## Dependencies
Database Connection Management

```python
@lru_cache(maxsize=1)
def get_db():
    """Get LangChain SQLDatabase instance with connection pooling"""
    if os.getenv("APP_ENV") == "ci":
        return MockSQLDatabase()
    try:
        return SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")

@lru_cache(maxsize=1)
def get_pymssql_connection() -> pymssql.Connection:
    return connect(host=MSSQL_HOST, server=MSSQL_SERVER, database=MSSQL_DATABASE)
```

**Features:**
- **Connection Pooling**: LRU cache for efficient connection reuse
- **Mock Support**: Automatic mock database for CI/testing
- **Error Handling**: Comprehensive connection failure handling
- **Dual Connections**: Both LangChain and PyODBC for different use cases


## Configuration

Connection string from `app.config`:

```python
MSSQL_CONNECTION_STRING = (
    f"mssql+pyodbc://{MSSQL_HOST}\\{MSSQL_SERVER}/{MSSQL_DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)

MSSQL_PYODBC_CONNECTION_STRING = (
    "DRIVER={SQL Server};"
    f"SERVER={MSSQL_HOST}\\{MSSQL_SERVER};"
    f"DATABASE={MSSQL_DATABASE};"
    "Trusted_Connection=yes;"
)
```

**Environment Variables:**
- `MSSQL_HOST` - Database server host (default: "localhost")
- `MSSQL_SERVER` - SQL Server instance (default: "SQLEXPRESS")  
- `MSSQL_DATABASE` - Database name (default: "northwind")

## Integration Points

- **Vector Store**: Seamless integration with Qdrant vector database
- **LLM Processing**: Uses Ollama for text generation
- **Embedding Generation**: Integrates with CLIP and text embedding services
- **Agent System**: Provides tools for agent-based database querying
- **FastAPI**: RESTful API endpoints for external integration

## Reference
- [Python drivers for SQL Server | Microsoft Learn](https://learn.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver17)
- [LangChain SQLDatabase Docs](https://python.langchain.com/api_reference/community/utilities/langchain_community.utilities.sql_database.SQLDatabase.html)
- [Setup SQL Server Auth (Chinese)](https://ithelp.ithome.com.tw/articles/10214386)
- [Window Defender Firewall for SQL Server](https://i-freelancer.net/WebHelp/Qboss/ACC40_WebHelp/SQLServerAw1.html)
- [Error: Adapve Server is unavalible](https://blog.csdn.net/vbwhere/article/details/103690794)
