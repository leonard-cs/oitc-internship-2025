from fastapi import HTTPException
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama

from backend.app.config import (
    MSSQL_CONNECTION_STRING,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_MODEL,
    backend_logger,
)
from backend.app.models.chat import AgentResponse, LLMResponse
from backend.app.prompts.prompts import get_rag_prompt
from backend.app.services.custom_agent_executor import CustomAgentExecutor
from backend.app.services.rag_llm import (
    execute_sql_query,
    generate_final_response,
    generate_sql_query,
    get_relevant_tables,
)

ollama = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
)


async def generate_answer_from_docs(query: str, docs: list[str]) -> LLMResponse:
    prompt_template = get_rag_prompt()

    structured_ollama = ollama.with_structured_output(LLMResponse)

    pipelines = (
        {"query": lambda x: x["query"], "context": lambda x: x["context"]}
        | prompt_template
        | structured_ollama
    )

    backend_logger.trace(f"Input variables: {prompt_template.input_variables}")
    backend_logger.trace(
        f"Prompt template:\n{prompt_template.format(query=query, context=docs)}"
    )
    response: LLMResponse = pipelines.invoke({"query": query, "context": docs})
    backend_logger.trace(response)
    backend_logger.success("Generated answer from LLM successfully")
    return response


async def generate_answer_from_sql(user_question: str):
    """Generate answer from SQL database with proper error handling."""
    relevant_tables = True
    regenerate_sql_query = True
    try:
        db = SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)
        table_list = db.get_usable_table_names()
        if relevant_tables:
            table_names = await get_relevant_tables(user_question, table_list)
        else:
            table_names = table_list
        table_info = db.get_table_info(table_names)

        sql_query = await generate_sql_query(user_question, table_info)
        query_results = await execute_sql_query(
            db, sql_query, user_question, table_info, regenerate_sql_query
        )
        final_response = await generate_final_response(user_question, query_results)

        return LLMResponse(answer=final_response, sources=table_names, log=sql_query)

    except Exception as e:
        error_msg = f"Error in SQL answer generation: {str(e)}"
        backend_logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


async def generate_answer(query: str) -> AgentResponse:
    agent = CustomAgentExecutor()
    try:
        response: AgentResponse = agent.invoke(query=query)
        return response
    except Exception as e:
        msg = f"Error occurred while generating answer: {e}"
        backend_logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)
