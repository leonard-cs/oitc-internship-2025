from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# Query Processing Prompts
QUERY_PROCESSING_SYSTEM_PROMPT = """You are an AI assistant that helps process and understand user queries.
You can classify queries, extract key information, and determine the best approach to handle them.
"""

# RAG Chain Prompts
RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.
Your responses should be concise and directly address the user's query.
If the context does not contain enough information to answer the question, respond with "I don't know."
\nContext: 
{context}
"""


def get_rag_prompt() -> ChatPromptTemplate:
    """Get the RAG chain prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(RAG_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )
