# Playground - A Modular AI Exploration Environment

Welcome to **playground**, a modular, extensible Python environment for experimenting with modern AI tools and architectures. Whether you're prototyping LangChain chains, building your own Model Context Protocol (MCP), or querying a local LLM using Ollama — this repo gives you clean, independent modules with shared utilities.

## Project Structure
```bash
playground/
├─ mssql/
├─ ollama/                          # Ollama query/embed playground
│   ├─ Dockerfile
│   ├─ ollama_init.sh
│   └─ main.py                      # python -m playground.ollama.main
├─ langchain/                       # Lanchain experiment
├─ query_process/                   # User query processor prototype with accuracy evaluator
├─ .env.example
└─ README.md
```
