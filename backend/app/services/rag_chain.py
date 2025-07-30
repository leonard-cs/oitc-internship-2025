from fastapi import HTTPException
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama

from backend.app.config import (
    MSSQL_CONNECTION_STRING,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_MODEL,
    backend_logger,
)
from backend.app.models.chat import (
    AgentResponse,
    FinalResponse,
    LLMResponse,
    SQLResponse,
    WhichTableResponse,
)
from backend.app.prompts.prompts import (
    get_rag_prompt,
    get_sql_query_prompt,
    get_sql_response_prompt,
    get_which_table_prompt,
)
from backend.app.services.custom_agent_executor import CustomAgentExecutor

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
    db = SQLDatabase.from_uri(MSSQL_CONNECTION_STRING)

    table_list = [
        "Categories",
        "Customers",
        "EmployeeTerritories",
        "Employees",
        "Order Details",
        "Orders",
        "Products",
        "Region",
        "Shippers",
        "Suppliers",
        "Territories",
    ]

    which_table_ollama = ollama.with_structured_output(WhichTableResponse)
    which_table_pipeline = (
        {
            "user_question": lambda x: x["user_question"],
            "table_list": lambda x: x["table_list"],
        }
        | get_which_table_prompt()
        | which_table_ollama
    )
    backend_logger.info("Generating which table response...")
    which_table_response: WhichTableResponse = which_table_pipeline.invoke(
        {"user_question": user_question, "table_list": table_list}
    )
    table_names = which_table_response.table_names
    backend_logger.debug(f"Table names: {table_names}")

    table_info = db.get_table_info(table_names)
    sql_ollama = ollama.with_structured_output(SQLResponse)
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
    backend_logger.debug(f"SQL query: {sql_query}")

    query_results = db.run_no_throw(sql_query)
    print(f"Query results:\n{query_results}")

    final_response_ollama = ollama.with_structured_output(FinalResponse)
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
    llm_results = final_response.response
    backend_logger.debug(f"LLM results: {llm_results}")
    return LLMResponse(answer=llm_results, sources=table_names)


async def generate_answer(query: str) -> AgentResponse:
    agent = CustomAgentExecutor()
    try:
        response: AgentResponse = agent.invoke(query=query)
        return response
    except Exception as e:
        msg = f"Error occurred while generating answer: {e}"
        backend_logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)
