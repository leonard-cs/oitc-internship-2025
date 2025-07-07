# OITC Internship 2025
A multi-service AI platform integrating chat, vector databases, and LLMs using Docker, PostgreSQL, MSSQL, and AnythingLLM.

## Project Structure
```bash
oitc-internship-2025/
├─ docker-compose.yml
├─ .env
├─ llm-server/                    # Python backend (MSSQL → AnythingLLM uploader)
│   ├─ Dockerfile
│   ├─ db_uploader/               # Scripts to extract from MSSQL & push to AnythingLLM
│   └─ requirements.txt
├─ chat-ui/
│   └─ Dockerfile                 # Next.js frontend
├─ anythingllm/
│   └─ config/
└─ README.md
```

## Getting Started
### 1. Prerequisites
Make sure you have:
- Docker installed
### 2. Environment Setup
Create a .env file in the root directory:
```bash
cp .env.example .env
```
### 3. Run the Project
In the root of the project (`oitc-internship-2025/`), run:
```bash
docker-compose up --build
```
This will spin up:
- PostgreSQL
- pgAdmin
- LLM Server (Python uploader)
- Chat UI (Next.js)
- Ollama (for local LLMs)
- AnythingLLM
### 4. Access Service
| Service     | URL                                              | Notes                            |
| ----------- | ------------------------------------------------ | -------------------------------- |
| Chat UI     | [http://localhost:3000](http://localhost:3000)   | Frontend app                     |
| AnythingLLM | [http://localhost:3001](http://localhost:3001)   | LLM interface                    |
| Ollama API  | [http://localhost:11434](http://localhost:11434) | Local model inference (REST API) |
| pgAdmin     | [http://localhost:5050](http://localhost:5050)   | DB Admin UI (use `db` as host)   |

<!-- | Service     | URL                                              | Description                                  |
| ----------- | ------------------------------------------------ | -------------------------------------------- |
| Chat UI     | [http://localhost:3000](http://localhost:3000)   | Frontend chat interface                      |
| LLM Server  | [http://localhost:8000](http://localhost:8000)   | Python service (uploads MSSQL → AnythingLLM) |
| AnythingLLM | [http://localhost:3001](http://localhost:3001)   | LLM document workspace & ingestion           |
| Ollama      | [http://localhost:11434](http://localhost:11434) | Local LLM API (e.g. llama3, mistral, etc.)   |
| pgAdmin     | [http://localhost:5050](http://localhost:5050)   | DB Admin UI (PostgreSQL)                     | -->
