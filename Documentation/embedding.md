# Embedding Models


## Overview
Embedding models are essential in natural language processing (NLP), enabling the transformation of text into numerical vector representations that capture the semantic meaning of the input. These vector embeddings allow for similarity search, clustering, and a range of downstream tasks.


## Embedding Models

### NomicEmbeddings
[LangChain Nomic Embedding Models Guide](https://python.langchain.com/docs/integrations/text_embedding/nomic/)

### OpenCLIP
[OpenClip](https://github.com/mlfoundations/open_clip/tree/main) is an source implementation of OpenAI's CLIP.
These multi-modal embeddings can be used to embed images or text.
See [Langchain's OpenClip Example](https://python.langchain.com/docs/integrations/text_embedding/open_clip/)

### Chinese (Traditional) Embeddings
See [Chinese (Traditional) Embeddings Review (Chinese)](https://ihower.tw/blog/12167-embedding-models)


## Table of Contents
- [Overview](#overview)
- [Embedding Models](#embedding-models-1)
- [Embedding Models in LangChain](#embedding-models-in-langchain)
- [Reference](#reference)


## Embedding Models in LangChain
LangChain provides built-in support for embedding models and includes methods to work with both queries and documents. For more details, refer to [LangChain’s Embedding How-To Guide](https://python.langchain.com/docs/how_to/#embedding-models).

### Core Methods
LangChain provides two primary methods for embedding text:
- `embed_documents()`: Embed multiple texts (documents)
- `embed_query()`: Embed a single text (query)

### Custom Embedding Class
To create a custom embedding model, implement the [embedding interface](https://python.langchain.com/api_reference/core/embeddings/langchain_core.embeddings.embeddings.Embeddings.html#langchain_core.embeddings.embeddings.Embeddings) provided by LangChain:
```python
class Embeddings(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed search docs.

        Args:
            texts: List of text to embed.

        Returns:
            List of embeddings.
        """

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """Embed query text.

        Args:
            text: Text to embed.

        Returns:
            Embedding.
        """
```
Example implementation: See `backend/app/embed/clipembedder.py` for a custom embedder.

### Limitations
LangChain’s built-in embeddings are text-only. To embed other data types (e.g., images), you must implement your own embedding logic.
For example, to embed an image, use a custom function like `encode_image()` (see: `backend/app/embed/clipembedder.py`).


## Reference
- [LangChain Embedding How-To Guide](https://python.langchain.com/docs/how_to/#embedding-models)
- [LangChain Built-In Embedding Models](https://python.langchain.com/docs/integrations/text_embedding/)
- [LangChain Embedding Interface Docs](https://python.langchain.com/api_reference/core/embeddings/langchain_core.embeddings.embeddings.Embeddings.html#langchain_core.embeddings.embeddings.Embeddings)
- [Embeddings Model 入門指南 (Chinese)](https://ithelp.ithome.com.tw/articles/10345537)
- [OpenCLIP Github](https://github.com/mlfoundations/open_clip/tree/main)
- [Langchain's OpenClip Example](https://python.langchain.com/docs/integrations/text_embedding/open_clip/)
- [LangChain's Nomic Embedding Guide](https://python.langchain.com/docs/integrations/text_embedding/nomic/)
- [Chinese (Traditional) Embeddings Review (Chinese)](https://ihower.tw/blog/12167-embedding-models)
