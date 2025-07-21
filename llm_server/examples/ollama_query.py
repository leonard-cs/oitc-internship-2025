# ollama_query.py
# python -m llm_server.examples.ollama_query

import requests

from llm_server.config import OLLAMA_BASE_URL, OLLAMA_MODEL

url = f"{OLLAMA_BASE_URL}/api/generate"

payload = {
    "model": OLLAMA_MODEL,
    "prompt": "why is sky blue",
    "stream": False,
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    response_data = response.json()
    print("Response:", response_data['response'])
else:
    print(f"Failed to get a response. Status code: {response.status_code}")