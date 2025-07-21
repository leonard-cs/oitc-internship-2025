```bash
backend/
├─ app/
│  ├─ routers/                  # API route definitions (grouped by feature)
│  │  ├─ chat.py                # /api/chat
│  │  ├─ query.py               # /api/query
│  │  ├─ embed.py               # /api/embed
│  │  ├─ extract.py             # /api/extract
│  │  └─ health.py              # /api/health
│  │
│  ├─ services/                 # Business logic and LangChain integration
│  │  ├─ chat.py                # Handles LLM + RAG
│  │  ├─ query_processor.py     # Semantic summarization
│  │  ├─ embedder.py            # Embedding pipeline
│  │  ├─ extractor.py           # MSSQL data extraction
│  │  └─ vectorstore.py         # Vector DB helpers
│  │
│  ├─ models/                   # Pydantic schemas (request/response)
│  │  ├─ chat.py
│  │  ├─ query.py
│  │  ├─ embed.py
│  │  └─ extract.py
│  │
│  ├─ config.py                 # Environment config, paths, secrets
│  └─ main.py                   # FastAPI app entrypoint
│
├─ tests/                       # All backend tests
│  ├─ test_chat.py
│  ├─ test_query.py
│  └─ ...
│
├─ requirements.txt
└─ README.md
```