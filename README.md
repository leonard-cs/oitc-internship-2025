# OITC Internship 2025
This project implements a chatbot that allows users to query a database using natural language. The system leverages the AnythingLLM and Ollama models for natural language understanding and response generation. Data from Microsoft SQL Server (MSSQL) tables is extracted and embedded into vector representations using AnythingLLM. These embeddings are stored in AnythingLLM's vector database, allowing the chatbot to efficiently retrieve relevant information based on semantic similarity and provide natural language responses. Additionally, the system features an image-based query functionality where users can upload images, and the chatbot will find similar images in the database by comparing their vector representations.

## Project Structure
```bash
oitc-internship-2025/
├─ llm-server/                    # Python backend
│   ├─ db_uploader/               # Extract data from MSSQL and push it to AnythingLLM
│   ├─ image_search/              # Image-based vector search logic
│   ├─ app.py                     # Main FastAPI application to handle image search
│   ├─ Dockerfile
│   └─ requirements.txt
├─ chat-ui/                       # Frontend built with Next.js
│   ├─ entrypoint.sh              # Entrypoint script to run Next.js app inside a container
│   └─ Dockerfile
├─ anythingllm/                   # AnythingLLM configuration and storage
│   ├─ .env.example
│   └─ storage/
├─ ollama/                        # LLM-based processing (Ollama container and API)
│   ├─ ollama-init.sh             # Initialization script for Ollama container
│   └─ Dockerfile
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
- PostgreSQL
- pgAdmin
- Chat UI (Next.js)
- Ollama (for local LLMs)
- AnythingLLM
<!-- - LLM Server (Python uploader) -->
### 4. Configure AnythingLLM
After the containers are running:
1. Visit http://localhost:3001/settings/api-keys
2. Click **"Generate New API Key"**
3. Copy the key
4. Paste it into your `.env` file:
```env
LLM_API_KEY=your_anythingllm_api_key
```
**Alternatively:**
- Navigate to Settings > Tools > Developer API
- Click "Generate New API Key"

Once added, restart the Chat UI container:
```bash
docker-compose restart chat-ui
```
### 5. Access Service
| Service     | URL                                              | Notes                            |
| ----------- | ------------------------------------------------ | -------------------------------- |
| Chat UI     | [http://localhost:3000](http://localhost:3000)   | Frontend app                     |
| AnythingLLM | [http://localhost:3001](http://localhost:3001)   | LLM interface                    |
| pgAdmin     | [http://localhost:5050](http://localhost:5050)   | DB Admin UI (use `db` as host)   |

<!-- | Service     | URL                                              | Description                                  |
| ----------- | ------------------------------------------------ | -------------------------------------------- |
| Chat UI     | [http://localhost:3000](http://localhost:3000)   | Frontend chat interface                      |
| LLM Server  | [http://localhost:8000](http://localhost:8000)   | Python service (uploads MSSQL → AnythingLLM) |
| AnythingLLM | [http://localhost:3001](http://localhost:3001)   | LLM document workspace & ingestion           |
| Ollama      | [http://localhost:11434](http://localhost:11434) | Local LLM API (e.g. llama3, mistral, etc.)   |
| pgAdmin     | [http://localhost:5050](http://localhost:5050)   | DB Admin UI (PostgreSQL)                     | -->

## Optional: Connect to pgAdmin
Only needed if you want to view or manage the database directly via a UI.
1. Open your browser and go to http://localhost:5050.
2. Login using the credentials from .env:
- **Email:** `PGADMIN_DEFAULT_EMAIL`
- **Password:** `PGADMIN_DEFAULT_PASSWORD`
3. Click **"Add New Server"**.
4. Under the **General** tab, set **Server Name** to `ps_db_docker` (or any name you prefer).
5. Switch to the **Connection** tab.
6. Run the following command in your terminal to find the IP address of the PostgreSQL container:
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' chat-ui-postgres
```
7. Copy the resulting IP address into the **Host name/address** field.
8. Enter the **Username** and **Password** exactly as set in your `.env` file (`POSTGRES_USER` and `POSTGRES_PASSWORD`).
