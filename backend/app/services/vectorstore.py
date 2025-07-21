async def retrieve_relevant_documents(query: str) -> tuple[list[str], list[str]]:
    # Simulate document retrieval
    docs = [f"Document {i} related to {query}" for i in range(1, 4)]
    sources = [f"Source {i}" for i in range(1, 4)]
    return docs, sources
