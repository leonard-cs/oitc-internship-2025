from app.chat.rag_llm import generate_final_response, get_relevant_tables
from app.config import backend_logger
from app.llm.models import RAGResponse, SQLRAGResponse
from app.llm.rag_services import (
    decide_collection,
    generate_answer_with_context,
    generate_sql_query,
)
from app.mssql.dependencies import get_SQLDatabase
from app.mssql.models import Table
from app.utils import documents_to_string
from app.vectorstore.service import search


async def vector_rag_pipeline(query: str) -> RAGResponse:
    backend_logger.info("Deciding which collection to search...")
    collection = decide_collection(query, Table.values())

    backend_logger.info(f"Searching collection: {collection}...")
    documents = search(query, collection)
    documents_string = documents_to_string(documents)

    backend_logger.info("Generating the answer...")
    return await generate_answer_with_context(query, documents_string)


async def sql_rag_pipeline(query: str):
    use_relevant_tables = True

    sql_db = get_SQLDatabase()
    all_table_names = sql_db.get_usable_table_names()

    if use_relevant_tables:
        backend_logger.info("Deciding relevant tables...")
        relevant_tables = await get_relevant_tables(query, all_table_names)
    else:
        relevant_tables = all_table_names

    table_info = sql_db.get_table_info(relevant_tables)

    backend_logger.info("Generating SQL query...")
    sql_query = await generate_sql_query(query, table_info)

    query_results = sql_db.run_no_throw(sql_query, fetch="all", include_columns=True)

    backend_logger.info("Generating final response...")
    sql_response = await generate_final_response(query, query_results)

    return SQLRAGResponse(answer=sql_response, sql=sql_query)
