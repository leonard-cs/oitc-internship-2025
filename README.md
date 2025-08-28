# OITC Internship 2025 - RAG AI Agent
This project implements a retrieval-augmented generation (RAG) chatbot that allows users to query MSSQL database content—including both text and images—using natural language or image inputs. Data from the database is extracted and converted into vector embeddings stored in Qdrant vector database for efficient semantic search. When a user submits a query, the system retrieves the most relevant information based on vector similarity and passes this context to the Ollama language model, which generates accurate, context-aware natural language responses. This combination of retrieval and generation enables the chatbot to deliver precise, up-to-date answers grounded in the underlying data while supporting image-based similarity search.

## Table of Contents
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [🚀 Quick Start](#-quick-start)
- [🎯 Getting Started](#-getting-started)

## Technology Stack
- ⚡ **FastAPI** for the Python backend API.
    - 🦜🔗 Integration with **LangChain** and **LangGraph** for advanced language model workflows
- 🚀 **React** for the frontend.
- 🦙 **Ollama** for LLM-based processing and containerized AI services
- 🧮 **Qdrant** as the vector database for semantic search and embeddings
- 🗄️ **Microsoft SQL Server (MSSQL)** Northwind database used for development and testing of data interactions
- 🐋 **Docker Compose** for development and production.
- ✅ Tests with **Pytest**.
- 🏭 **CI/CD** pipelines configured with **GitHub Actions**.

## Project Structure
```bash
oitc-internship-2025/
├─ backend/                         # FastAPI backend
│   ├─
│   └─
│
├─ frontend/                        # Next.js frontend
│   ├─
│   └─
│
├─ ollama/                          # Ollama container
│   ├─ ollama-init.sh               # Initialization script for Ollama container
│   └─ Dockerfile
│
├─ Documentation/
│
├─ .env.example
├─ .gitignore
├─ docker-compose.yml
└─ README.md
```

## 🚀 Quick Start
⚠️ Currently tested on **Windows** only.
### 1. Prerequisites
Make sure you have the following installed:
- [Docker](https://www.docker.com/products/docker-desktop/)
- [pnpm](https://pnpm.io/installation)

Additionally, set up MSSQL SQL Server Authentication. For more details, refer to the [MSSQL Setup Guide](./Documentation/mssql.md).

### 2. Environment Setup
Copy the example environment file and update values as needed:
```bash
cp .env.example .env
```
### 3. Running the Project
To start the project, follow these steps:
1. In the root directory of the project (`oitc-internship-2025/`), run:
    ```bash
    docker-compose up -d
    ```
    This will start the following services:
    - Backend (FastAPI)
    - Ollama (for local LLMs)
    - Qdrant (vector database)

2. In the frontend/ directory, install the necessary dependencies and start the development server:
    ```bash
    pnpm install
    pnpm next-dev
    ```

### 4. Using a Local Backend (Optional)
If MSSQL is not accessible (e.g., due to firewall restrictions):
1. **Stop the docker backend service:**
    ```bash
    docker compose stop backend
    ```
2. **Set up the local backend** by running the following command to start a local FastAPI server:
    ```bash
    cd backend/
    uv run fastapi dev
    ```

### 5. Accessing the Services
Here are the URLs for the available services:
| Service     | URL                                                                     | Notes                 |
| ----------- | ----------------------------------------------------------------------- | --------------------- |
| Backend     | [http://localhost:8000/docs#/](http://localhost:8000/docs#/)            | FastAPI API docs      |
| Frontend    | [http://localhost:3000](http://localhost:3000)                          | Chat UI               |
| Qdrant      | [http://localhost:6333/dashboard#/](http://localhost:6333/dashboard#/)  | Qdrant dashboard      |

## 🎯 Getting Started
### 1. Sync MSSQL to Vector Database
Update the tables enum and SQL queries in `/backend/app/mssql/models.py` to match your database schema.

Execute the [AI Sync All endpoint](http://localhost:8000/docs#/mssql/ai_sync_all_api_v1_mssql_ai_sync_all__post) to load data from MSSQL into Qdrant.

### 2. Verify Vector Store
Call the [Vector Store Info endpoint](http://localhost:8000/docs#/vectorstore/get_info_api_v1_vectorstore_info_get) to confirm sync success.

### 3. Chat with RAG
Try different endpoints:
- [vector-rag-query](http://localhost:8000/docs#/chat/vector_rag_query_api_v1_chat_vector_rag_query_post)
- [sql-rag-query](http://localhost:8000/docs#/chat/vector_rag_query_api_v1_chat_sql_rag_query_post)
- [image-query](http://localhost:8000/docs#/chat/image_query_api_v1_chat_image_query_post)
- [stream-chat](http://localhost:8000/docs#/chat/stream_chat_api_v1_chat_stream_chat_post)

### 4. Use the Agent
Call the [ask_agent endpoint](http://localhost:8000/docs#/agent/ask_chat_agent_api_v1_agent_ask_agent_post) or use the [frontend chat interface](http://localhost:3000).

## Backend Development
Backend docs: [backend/README.md](./backend/README.md).

## Frontend Development
Frontend docs: [frontend/README.md](./frontend/README.md).

## Deployment
Deployment docs: [deployment.md](./deployment.md).

## Development
General development docs: [development.md](./development.md).
