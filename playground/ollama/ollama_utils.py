import requests

from playground.config import OLLAMA_BASE_URL, PHI3, NOMIC

def gen_embedding(input: str, model: str = NOMIC) -> list[float]:
    payload = {
        "model": model,
        "input": input,
    }

    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/embed", json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad status codes
        data = response.json()

        embeddings = data.get("embeddings")
        if not embeddings or not isinstance(embeddings, list):
            raise ValueError("Invalid response format: 'embeddings' key missing or not a list.")

        return embeddings[0]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
    
# text = "Product #1 is called 'Chai' priced at $18.00 with 39 units in stock and it is currently available."
# print(gen_embedding(text))

def query_with_contexts(context: list[str], question: str, model: str = PHI3) -> str:
    combined_context = "\n".join(context)

    prompt = f"""Use the context below to answer the question.

            Context:
            {combined_context}

            Question:
            {question}
            """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error querying Ollama: {e}"
