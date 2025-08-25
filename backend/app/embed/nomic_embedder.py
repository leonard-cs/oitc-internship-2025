# llm_server/embeddings/nomic_embedder.py

import requests


class NomicEmbedder:
    def __init__(self, model="nomic-embed-text", base_url="http://localhost:11434"):
        self.model = model
        self.url = f"{base_url}/api/embed"

    def embed_text(self, text: str) -> list[float]:
        payload = {"model": self.model, "input": text}
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            embedding = response.json().get("embeddings", [])[0]
            return embedding
        except Exception as e:
            print(f"Failed to generate embedding: {e}")
            return []

    def embed_image(self, image_path: str) -> list[float]:
        raise NotImplementedError("OllamaEmbedder does not support image embeddings.")


if __name__ == "__main__":
    print(len(NomicEmbedder().embed_text("Hi")))
