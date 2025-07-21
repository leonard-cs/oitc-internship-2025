from backend.app.models.chat import ChatResponse


async def handle_chat_request(
    user_query: str, use_query_processor: bool = True
) -> ChatResponse:
    if use_query_processor:
        semantic_query = "Processed query based on user input"
    else:
        semantic_query = user_query
    return ChatResponse(
        answer="Sample answer based on user query",
        semantic_query=semantic_query,
        sources=["source1", "source2"],
    )
