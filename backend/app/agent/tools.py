from app.agent.models import AgentResponse
from app.config import backend_logger
from app.mssql.dependencies import get_db
from app.mssql.models import Table
from app.vectorstore.service import get_vectorstore, search
from langchain_core.documents import Document
from langchain_core.tools import tool


@tool
def vector_search(query: str, table_name: str) -> list[Document]:
    """
    Perform a vector similarity search against a set of documents.
    The query should contain the semantic meaning of original query.
    Returns top 5 most relevant context documents and their sources.
    You should use get_table_names tool to get the table names if uou are not sure about the table name.
    This tool will convert the query to vector.
    This tool dont need to know the table schema.
    """
    backend_logger.info("Executing 'vector_search' tool")

    qdrant = get_vectorstore()
    if not qdrant.collection_exists(table_name):
        return f"Table {table_name} does not exist.\nAvailable tables: {qdrant.get_collections()}"

    documents: list[Document] = search(query, table_name)
    return documents


@tool
def get_table_names() -> list[str]:
    """
    Get the names of the tables.
    Return the names of the tables.
    """
    return [table.value for table in Table]


@tool
def get_table_schema(table_names: list[Table]) -> str:
    """
    Get the schema of the table.
    Return the schema of the table.
    """
    return get_db().get_table_info(table_names)


@tool
def execute_sql_tool(sql_query: str) -> str:
    """
    Execute a SQL query against the database.
    Return the result of the query.
    """
    return get_db().run_no_throw(sql_query)


@tool
def direct_answer(answer: str, sources: list[str], tools_used: list[str]):
    """Use this tool to provide a direct answer to the user for general knowledge questions, greetings
    , or the llm already knows the answer.
    The answer should be in natural language as this will be provided to the user directly.
    The `tools_used` parameter must include a list of tool names utilized in the `scratchpad`(excluding `direct_answer`).
    The `sources` parameter must include a list of source document references used.
    """
    return AgentResponse(answer=answer, sources=sources, tools_used=tools_used)


tools = [
    direct_answer,
    vector_search,
    get_table_names,
    get_table_schema,
    execute_sql_tool,
]
