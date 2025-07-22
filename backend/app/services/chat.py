from backend.app.models.chat import ChatResponse, LLMResponse
from backend.app.services.embed.embedder import get_embeddings
from backend.app.services.query_processor import process_query
from backend.app.services.rag_chain import generate_answer_from_docs
from backend.app.services.vectorstore import retrieve_relevant_documents


async def handle_chat_request(
    user_query: str, use_query_processor: bool = True
) -> ChatResponse:
    # TODO: process user query
    semantic_query = user_query
    if use_query_processor:
        semantic_query = await process_query(user_query)
    # TODO: embed processed query
    query_embedding: list[float] = get_embeddings(text=semantic_query).text_embedding
    # TODO: retrieve relevant documents
    docs, sources = await retrieve_relevant_documents(query_embedding)
    response: LLMResponse = await generate_answer_from_docs(
        query=semantic_query, docs=docs
    )

    return ChatResponse(
        answer=response.answer,
        semantic_query=semantic_query,
        sources=sources,
    )
