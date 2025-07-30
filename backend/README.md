## Project Structure
```bash
backend/
├── app/
│   ├── main.py
│   ├── config.py                       # Application configuration
│   │
│   ├── embed/                          # Embedding functionality module
│   │   ├── routes.py                   # API endpoints
│   │   ├── models.py                   # Data models
│   │   ├── service.py                  # Business logic
│   │   ├── save_model.py               # Model persistence utilities
│   │   └── clipembedder.py             # CLIP embedding implementation
│   │
│   ├── vectorstore/
│   │   ├── ...
│   │   └── utils.py                    # Vectorstore utility functions
│   │
│   ├── chat/
│   │   ├── ...
│   │   ├── query_processor.py          # Query processing logic
│   │   ├── rag_chain.py                # RAG (Retrieval-Augmented Generation) chain
│   │   └── rag_llm.py                  # RAG LLM integration
│   │
│   ├── agent/
│   │   ├── ...
│   │   └── custom_agent_executor.py    # Custom agent execution logic
│   │
│   └── api/                            # API versioning and routing
│       └── v1/                         # API versioning and routing
│           └── api.py                  # V1 API router and endpoint includes
│
├── tests/                              # Test suite
│   ├── e2e/
│   └── unittest/
└── README.md
```
