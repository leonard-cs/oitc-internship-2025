## Ollama APIs
https://github.com/ollama/ollama/blob/main/docs/api.md

## Ollama Code
### Query
```python
payload = {
    "model": OLLAMA_MODEL,
    "prompt": "why is sky blue",
    "stream": False,
}
response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
data = response.json()
print("Response:", data['response'])
```
### Embedding
```python
payload = {
    "model": model,
    "input": "Why is the sky blue?",
}
response = requests.post(f"{OLLAMA_BASE_URL}/api/embed", json=payload)
data = response.json()
print("Embedding:", data["embeddings"][0])
```