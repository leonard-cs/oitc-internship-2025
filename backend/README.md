# 🤖 Agentic RAG - Backend

## Overview
This backend provides a Retrieval-Augmented Generation (RAG) service with an 
agentic workflow and multimodal capabilities. It serves as a comprehensive data intelligence hub that bridges structured databases, unstructured documents, and AI-powered analysis.

**Core Technologies:**
- **FastAPI** → High-performance REST API layer with automatic OpenAPI documentation
- **LangChain** → Orchestration framework for building LLM-powered applications
- **Ollama** → Local large language model inference
- **Qdrant** → Vector database for document storage & retrieval

**Key Capabilities:**
- Intelligent agents with dynamic tool use (vector search, schema inspection, SQL search) and iterative reasoning
- Semantic and multimodal search across text, images, and structured data using CLIP embeddings
- Automated MSSQL-to-vector sync, and AI-powered data extraction
- REST API versioning, health monitoring, modular design, and Docker deployment

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Architecture & Design](#architecture--design)
- [Installation & Setup](#installation--setup)
- [Models](#models)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [References](#reference)


## Project Structure
```bash
module/
├── routes.py       # API endpoints
├── models.py       # Data models
└── service.py      # Business logic
```
```bash
backend/
├── app/
│   ├── embed/                          # Embedding functionality module
│   │   ├── ...
│   │   ├── save_model.py               # Model persistence utilities
│   │   └── clipembedder.py             # CLIP embedding implementation
│   │
│   ├── mssql/
│   │   ├── ...
│   │   ├── dependencies.py
│   │   └── utils.py
│   │
│   ├── vectorstore/
│   │   ├── ...
│   │   ├── qdrant_vectorstore.py
│   │   └── utils.py                    # Vectorstore utility functions
│   │
│   ├── rag_system/
│   │   └── pipelines.py
│   │
│   ├── llm/
│   │   ├── ...
│   │   ├── ollama.py
│   │   ├── prompts.py
│   │   └── rag_services.py
│   │
│   ├── chat/
│   │   ├── ...
│   │   ├── query_processor.py          # Query processing logic
│   │   └── rag_llm.py                  # RAG LLM integration
│   │
│   ├── agent/
│   │   ├── ...
│   │   ├── custom_agent_executor.py    # Custom agent execution logic
│   │   ├── tools.py
│   │   └── utils.py
│   │
│   ├── api/                            # API versioning and routing
│   │   └── v1/
│   │       └── api.py
│   │
│   ├── config.py                       # Application configuration
│   └── main.py
│
├── tests/                              # Test suite
│   ├── e2e/
│   └── services/
│
├── Dockerfile
├── .dockerignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```


## Architecture & Design
### Document Processing
<!-- ![](/Documentation/images/Document%20Preprocessing.png) -->

<div align="center>
    <img src="/Documentation/images/Document Preprocessing.png" alt="Documant Processing Pipeline" width="600"/>
</div>

### Document Retreval
<div align="center>
    <img src="/Documentation/images/Vector Search.png" alt="Documant Retreval Pipeline" width="600"/>
</div>

### SQL Search
<div align="center>
    <img src="/Documentation/images/SQL Search.png" alt="SQL Search Pipeline" width="600"/>
</div>

### Agentic loop
<div align="center>
    <img src="/Documentation/images/Agent Pipeline.png" alt="Agent Pipeline" width="600"/>
</div>

## Models
This system relies on a suite of powerful, open-source models.

Muti-model Embedding; open-clip...
Thinking Model: qwen; ollama


## API Endpoints


## Usage


## Roadmap
✅ Support chat streaming\
🔲 Support agent streaming
🔲 Custom agent loop for improved control

## Reference
- [UV Docs](https://docs.astral.sh/uv/)
- [FastAPI Docs](https://fastapi.tiangolo.com/reference/)
- [LangChain Docs](https://python.langchain.com/api_reference/)
- [Ollama Docs](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [Qdrant Docs](https://qdrant.tech/documentation/)
