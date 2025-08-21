from app.chat.rag_llm import (
    execute_sql_query,
    generate_final_response,
    generate_sql_query,
    get_relevant_tables,
)
from app.config import backend_logger
from app.llm.models import CollectionDecisionResponse, RAGResponse
from app.llm.ollama import get_ollama
from app.llm.prompts import get_collection_decision_prompt, get_rag_prompt
from app.mssql.dependencies import get_SQLDatabase
from fastapi import HTTPException


def decide_collection(query: str, tables: list[str]) -> str:
    decide_collection_prompt = get_collection_decision_prompt()
    structured_ollama = get_ollama().with_structured_output(CollectionDecisionResponse)

    pipelines = (
        {"query": lambda x: x["query"], "collections": lambda x: x["collections"]}
        | decide_collection_prompt
        | structured_ollama
    )

    collection_response: CollectionDecisionResponse = pipelines.invoke(
        {"query": query, "collections": tables}
    )
    backend_logger.trace(collection_response)
    return collection_response.collection


async def generate_answer_with_context(query: str, context: str) -> RAGResponse:
    prompt_template = get_rag_prompt()
    structured_ollama = get_ollama().with_structured_output(RAGResponse)

    pipelines = (
        {"query": lambda x: x["query"], "context": lambda x: x["context"]}
        | prompt_template
        | structured_ollama
    )

    # backend_logger.trace(
    #     f"Prompt template:\n{prompt_template.format(query=query, context=context)}"
    # )

    response: RAGResponse = pipelines.invoke({"query": query, "context": context})
    backend_logger.trace(response)

    return response


async def generate_answer_from_sql(user_question: str):
    """Generate answer from SQL database with proper error handling."""
    # TODO: move get_relevant_tables from chat/rag_llm.py to this file
    # TODO: move generate_sql_query from chat/rag_llm.py to this file

    relevant_tables = True
    regenerate_sql_query = True
    try:
        sqldatabase = get_SQLDatabase()
        table_list = sqldatabase.get_usable_table_names()

        if relevant_tables:
            table_names = await get_relevant_tables(user_question, table_list)
        else:
            table_names = table_list

        table_info = sqldatabase.get_table_info(table_names)
        backend_logger.trace(f"Table info: {table_info}")

        sql_query = await generate_sql_query(user_question, table_info)
        query_results, sql_query = await execute_sql_query(
            sqldatabase, sql_query, user_question, table_info, regenerate_sql_query
        )
        final_response = await generate_final_response(user_question, query_results)

        return RAGResponse(answer=final_response, sources=table_names, log=sql_query)

    except Exception as e:
        error_msg = f"Error in SQL answer generation: {str(e)}"
        backend_logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
