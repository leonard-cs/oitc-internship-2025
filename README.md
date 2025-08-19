# OITC Internship 2025
This project implements a retrieval-augmented generation (RAG) chatbot that allows users to query MSSQL database content—including both text and images—using natural language or image inputs. Data from the database is extracted and converted into vector embeddings stored in Qdrant vector database for efficient semantic search. When a user submits a query, the system retrieves the most relevant information based on vector similarity and passes this context to the Ollama language model, which generates accurate, context-aware natural language responses. This combination of retrieval and generation enables the chatbot to deliver precise, up-to-date answers grounded in the underlying data while supporting image-based similarity search.

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
- Docker
### 2. Environment Setup
Copy the example environment file and update values as needed:
```bash
cp .env.example .env
```
### 3. Run the Project
In the root of the project (`oitc-internship-2025/`), run:
```bash
docker-compose up -d
```
This will spin up:
<!-- - Frontend (Next.js) -->
- Backend (FastAPI)
- Ollama (for local LLMs)
- Qdrant (vector database)
### 4. Access Service
| Service     | URL                                                             | Notes                            |
| ----------- | --------------------------------------------------------------- | -------------------------------- |
| Backend     | [http://localhost:8000/docs#/](http://localhost:8000/docs#/)    | FastAPI documents                |

<!-- | Service     | URL                                                             | Notes                            |
| ----------- | --------------------------------------------------------------- | -------------------------------- |
| Frontend    | [http://localhost:3000](http://localhost:3000)                  | Frontend app                     |
| Backend     | [http://localhost:8000/docs#/](http://localhost:8000/docs#/)    | FastAPI documents                | -->

## Backend Development
Backend docs: [backend/README.md](./backend/README.md).

## Frontend Development
Frontend docs: [frontend/README.md](./frontend/README.md).

## Deployment
Deployment docs: [deployment.md](./deployment.md).

## Development
General development docs: [development.md](./development.md).
