# OITC Internship 2025
This project implements a retrieval-augmented generation (RAG) chatbot that allows users to query MSSQL database content—including both text and images—using natural language or image inputs. Data from the database is extracted and converted into vector embeddings stored in Qdrant vector database for efficient semantic search. When a user submits a query, the system retrieves the most relevant information based on vector similarity and passes this context to the Ollama language model, which generates accurate, context-aware natural language responses. This combination of retrieval and generation enables the chatbot to deliver precise, up-to-date answers grounded in the underlying data while supporting image-based similarity search.

## Table of Contents
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)

## Project Structure
```bash
oitc-internship-2025/
├─ backend/                         # FastAPI backend
│   ├─
│   └─
├─ frontend/                        # Next.js frontend
│   ├─
│   └─
├─ weights/                         # Storing embedder (.gitignore)
│   └─
├─ llm_server/                      # Python backend v1 (not used)
│   ├─ db_uploader/                 # Extract data from MSSQL and push it to AnythingLLM
│   ├─ image_search/                # Image-based vector search logic
│   ├─ app.py                       # Main FastAPI application to handle image search
│   ├─ Dockerfile
│   └─ requirements.txt
├─ chat-ui/                         # Frontend built with Next.js v1 (not used)
│   ├─ entrypoint.sh                # Entrypoint script to run Next.js app inside a container
│   └─ Dockerfile                      # Embed data and push to vector store
├─ anythingllm/                     # AnythingLLM configuration and storage
│   ├─ .env.example
│   └─ storage/
├─ ollama/                          # LLM-based processing (Ollama container and API)
│   ├─ ollama-init.sh               # Initialization script for Ollama container
│   └─ Dockerfile
├─ playground/                      #
│   └─
├─ docker-compose.yml
├─ .env.example
└─ README.md
```

## Getting Started
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

### 4. Verifying MSSQL Connection
Before proceeding, ensure that MSSQL is accessible. If the firewall isn't properly configured or you're unable to connect to MSSQL, you can use a local backend instead of the default one.

**To use a local backend:**
1. **Stop the backend service:**
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
| Backend     | [http://localhost:8000/docs#/](http://localhost:8000/docs#/)            | FastAPI documentation     |
| Frontend    | [http://localhost:3000](http://localhost:3000)                          | Chat interface        |
| Qdrant      | [http://localhost:6333/dashboard#/](http://localhost:6333/dashboard#/)  | Qdrant dashboard      |

## Backend Development
Backend docs: [backend/README.md](./backend/README.md).

## Frontend Development
Frontend docs: [frontend/README.md](./frontend/README.md).

## Deployment
Deployment docs: [deployment.md](./deployment.md).

## Development
General development docs: [development.md](./development.md).
