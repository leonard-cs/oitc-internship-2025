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
│   ├─ entrypoint.sh
│   └─ Dockerfile                 # Next.js frontend
├─ anythingllm/
│   ├─ .env
│   └─ storage/
├─ ollama/
│   ├─ ollama-init.sh
│   └─ Dockerfile
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
