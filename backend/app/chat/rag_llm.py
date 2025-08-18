from app.chat.models import (
    FinalResponse,
    RelevantTablesResponse,
    SQLResponse,
)
from app.config import backend_logger
from app.llm.ollama import get_ollama
from app.llm.prompts import (
    get_regenerate_sql_query_prompt,
    get_relevant_tables_prompt,
    get_sql_query_prompt,
    get_sql_response_prompt,
)
from fastapi import HTTPException
from langchain_community.utilities import SQLDatabase


async def get_relevant_tables(user_question: str, table_list: list[str]) -> list[str]:
    """Get relevant table names based on the user question."""
    table_ollama = get_ollama().with_structured_output(RelevantTablesResponse)
    table_pipeline = (
        {
            "user_question": lambda x: x["user_question"],
            "table_list": lambda x: x["table_list"],
        }
        | get_relevant_tables_prompt()
        | table_ollama
    )

    backend_logger.info("Determining relevant tables...")
    table_response: RelevantTablesResponse = table_pipeline.invoke(
        {"user_question": user_question, "table_list": table_list}
    )
    relevant_tables = table_response.relevant_tables
    backend_logger.debug(f"\nRelevant tables: {relevant_tables}")
    return relevant_tables


async def generate_sql_query(user_question: str, table_info: str) -> str:
    try:
        sql_ollama = get_ollama().with_structured_output(SQLResponse)
        sql_query_pipeline = (
            {
                "user_question": lambda x: x["user_question"],
                "table_info": lambda x: x["table_info"],
            }
            | get_sql_query_prompt()
            | sql_ollama
        )
        backend_logger.info("Generating SQL query response...")
        sql_response: SQLResponse = sql_query_pipeline.invoke(
            {"user_question": user_question, "table_info": table_info}
        )
        sql_query = sql_response.sql_query
        backend_logger.debug(f"SQL query:\n{sql_query}")
        return sql_query
    except Exception as e:
        error_msg = f"Error generating SQL query: {str(e)}"
        backend_logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


async def _regenerate_sql_query_with_error(
    user_question: str, table_info: str, error_message: str
) -> str:
    """Regenerate SQL query with error context from previous failed attempt."""
    try:
        sql_ollama = get_ollama().with_structured_output(SQLResponse)
        sql_query_pipeline = (
            {
                "user_question": lambda x: x["user_question"],
                "table_info": lambda x: x["table_info"],
                "error_message": lambda x: x["error_message"],
            }
            | get_regenerate_sql_query_prompt()
            | sql_ollama
        )
        sql_response: SQLResponse = sql_query_pipeline.invoke(
            {
                "user_question": user_question,
                "table_info": table_info,
                "error_message": error_message,
            }
        )
        sql_query = sql_response.sql_query
        backend_logger.debug(f"Regenerated SQL query:\n{sql_query}")
        return sql_query
    except Exception as e:
        error_msg = f"Error regenerating SQL query: {str(e)}"
        backend_logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


async def execute_sql_query(
    db: SQLDatabase, sql_query: str, user_question: str, table_info: str, retry: bool
) -> tuple[str, str]:
    """Execute SQL query and return results."""
    sql_query = sql_query
    if not retry:
        query_results = db.run_no_throw(sql_query, fetch="all", include_columns=True)
        backend_logger.trace(f"Query results:\n{query_results}")
        return query_results, sql_query

    max_attempts = 3
    current_attempt = 1

    while current_attempt <= max_attempts:
        try:
            query_results = db.run(sql_query)
            backend_logger.trace(f"Query results:\n{query_results}")
            return query_results, sql_query
        except Exception as e:
            error_str = str(e)
            backend_logger.warning(
                f"SQL execution failed on attempt {current_attempt}:\n{error_str}"
            )

            if current_attempt == max_attempts:
                error_msg = (
                    f"SQL execution failed after {max_attempts} attempts:\n{error_str}"
                )
                backend_logger.error(error_msg)
                return error_msg, sql_query

            # Regenerate SQL query with error context
            backend_logger.info(
                f"Regenerating SQL query (attempt {current_attempt + 1})..."
            )
            sql_query = await _regenerate_sql_query_with_error(
                user_question, table_info, str(e)
            )
            current_attempt += 1


async def generate_final_response(user_question: str, query_results: str) -> str:
    """Generate final response from query results."""
    final_response_ollama = get_ollama().with_structured_output(FinalResponse)
    final_response_pipeline = (
        {
            "user_question": lambda x: x["user_question"],
            "query_results": lambda x: x["query_results"],
        }
        | get_sql_response_prompt()
        | final_response_ollama
    )
    backend_logger.info("Generating final response...")
    final_response: FinalResponse = final_response_pipeline.invoke(
        {"user_question": user_question, "query_results": query_results}
    )
    return final_response.response
