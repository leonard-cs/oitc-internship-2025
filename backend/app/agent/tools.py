from langchain_core.documents import Document
from langchain_core.tools import tool

from backend.app.agent.models import AgentResponse
from backend.app.config import backend_logger
from backend.app.embed.service import get_embeddings
from backend.app.mssql.dependencies import get_db
from backend.app.mssql.services import execute_sql, fetch_table_info, fetch_table_names
from backend.app.vectorstore.service import search


@tool
def vector_search(query: str, collection_name: str) -> list[Document]:
    """
    Perform a vector similarity search against a set of documents.
    The query should contain the semantic meaning of original query.
    collection_name can be "Products" or "Employees"
    Returns top 5 most relevant context documents and their sources.
    """
    backend_logger.info("Executing 'vector_search' tool")
    documents: list[Document] = search(query, collection_name)
    return documents


@tool
def gen_embedding(text: str) -> list:
    """
    Generate an embedding of a text.
    Return embeddings
    """
    result = get_embeddings(text=text)
    return result.text_embedding


@tool
def get_table_info(table_names: list[str]) -> str:
    """
    Get the information of the table.
    Return the information of the table.
    """
    db = get_db()
    return fetch_table_info(db, table_names)
    # return fetch_table_info(db, fetch_table_names(db))


@tool
def execute_sql_tool(sql_query: str) -> str:
    """
    Execute a SQL query against the database.
    Return the result of the query.
    """
    db = get_db()
    return execute_sql(db, sql_query)


@tool
def final_answer(answer: str, sources: list[str], tools_used: list[str]):
    """Use this tool to provide a final answer to the user.
    The answer should be in natural language as this will be provided
    to the user directly. The tools_used must include a list of tool
    names that were used within the `scratchpad`.
    """
    return AgentResponse(answer=answer, sources=sources, tools_used=tools_used)


tools = [final_answer, vector_search, get_table_info, execute_sql_tool]
