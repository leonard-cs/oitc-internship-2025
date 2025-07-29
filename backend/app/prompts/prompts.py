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
def get_rag_prompt() -> ChatPromptTemplate:
    """Get the RAG chain prompt template."""

    RAG_SYSTEM_PROMPT = """
        You are a helpful assistant that answers questions based on the provided context.
        Your responses should be concise and directly address the user's query.
        If the context does not contain enough information to answer the question, respond with "I don't know."
        
        Context: 
        {context}
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(RAG_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )


# SQL Query Prompts
def get_which_table_prompt() -> ChatPromptTemplate:
    """Get the which table prompt template."""

    WHICH_TABLE_SYSTEM_PROMPT = """
        You are an AI assistant designed to decide which sql tables are relevant to the user's question.
        Table list:
        {table_list}
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(WHICH_TABLE_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("{user_question}"),
        ]
    )


def get_sql_query_prompt() -> ChatPromptTemplate:
    """Get the SQL query generation prompt template."""

    SQL_QUERY_SYSTEM_PROMPT = """
        You are an AI assistant designed to interact with a SQL Server database.
        You have access to the following tables and their schemas:

        Table info:
        {table_info}

        Given a user's question, generate a syntactically correct SQL query to retrieve the relevant information.
        - Use **PascalCase** for all table and column names exactly as shown in table info. (e.g., OrderDate, CustomerID)
        - Do NOT use snake_case or any other naming conventions.
        - Limit your query to at most 5 rows unless the user specifies otherwise.
        - Only query the necessary columns and tables relevant to the question.
        - Do NOT perform any data modification operations (INSERT, UPDATE, DELETE, DROP).
        - Double-check your query for correctness.
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(SQL_QUERY_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("{user_question}"),
        ]
    )


def get_sql_response_prompt() -> ChatPromptTemplate:
    """Get the SQL response generation prompt template."""

    SQL_RESPONSE_SYSTEM_PROMPT = """
        You are an AI assistant with access to the results of a SQL query executed against a database.

        User's question:
        {user_question}

        SQL query results:
        {query_results}

        Based on the results, provide a clear, concise, and relevant answer to the user's question.
        - If the results are empty or do not answer the question, say you don't know.
        - Do NOT repeat the SQL query or the raw data unless necessary for clarity.
        - Keep the answer brief and focused on the user's intent.
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(SQL_RESPONSE_SYSTEM_PROMPT),
        ]
    )
