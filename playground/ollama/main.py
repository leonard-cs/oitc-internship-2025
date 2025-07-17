# python -m playground.ollama.main
from playground.ollama.qdrant_ollama import create_collection, save_embedding, search_similar
from playground.ollama.ollama_utils import gen_embedding, query_with_contexts
from playground.ollama.utils import extract_payload_texts

data = [
    "Product #1 is called 'Chai' priced at $18.00 with 39 units in stock and it is currently available.",
    "Product #2 is called 'Chang' priced at $19.00 with 17 units in stock and it is currently available.",
    "Product #3 is called 'Aniseed Syrup' priced at $10.00 with 13 units in stock and it is currently available.",
    "Product #4 is called 'Chef Anton's Cajun Seasoning' priced at $22.00 with 53 units in stock and it is currently available.",
    "Product #5 is called 'Chef Anton's Gumbo Mix' priced at $21.35 with 0 units in stock and it has been discontinued.",
]

# Save data to vector database
create_collection()
for index, text in enumerate(data):
    embeddings = gen_embedding(text)
    save_embedding(embedding=embeddings, metadata={'text': text})

query = "Tell me abt Chai"
query_embeddings = gen_embedding(query)
result = search_similar(query_embeddings, limit=2)
context = extract_payload_texts(result)
response = query_with_contexts(context, question=query)
print(response)
