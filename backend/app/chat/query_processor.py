from app.chat.models import QueryProcessorResponse
from app.config import backend_logger
from app.llm.ollama import get_ollama
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough

ollama = get_ollama()
structured_ollama = ollama.with_structured_output(QueryProcessorResponse)

system_prompt = SystemMessagePromptTemplate.from_template("""
You are a query processor designed to clean up natural language user queries for a database-driven chatbot.
Your goal is to remove irrelevant information, side comments, filler words, or emotional context and return only the essential query content that should be used to retrieve data from a database.
Focus only on the user's intent related to querying structured data such as tables (e.g., orders, customers, products, employees). Your output should be a short, focused string that captures the core query, as if it were a database question.
Do not include greetings, opinions, excuses, unrelated backstories, or expressions like “I think”, “just wondering”, “can you”, etc. Only include details relevant to the query (entities, filters, fields, values, timeframes, etc.).
Output only the cleaned query string.
""")

examples = [
    {
        "user_query": "Hey! I was looking over the product catalog and just got curious — are there any products that are currently out of stock?",
        "output": "products that are currently out of stock",
    },
    {
        "user_query": "Before I forget again, could you tell me which employees joined after January 2023? Sorry, it's for my report!",
        "output": "employees who joined after January 2023",
    },
    {
        "user_query": "I hope this isn't a dumb question, but is there a way to list all customers from California who haven't made a purchase this year?",
        "output": "customers from California with no purchases this year",
    },
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{user_query}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

user_prompt = HumanMessagePromptTemplate.from_template(
    "Extract the main topic and key concepts from the following query:\n{user_query}",
    input_variables=["user_query"],
)

prompt = ChatPromptTemplate.from_messages([system_prompt, few_shot_prompt, user_prompt])

chain = {"user_query": RunnablePassthrough()} | prompt | structured_ollama


async def process_query(query: str) -> QueryProcessorResponse:
    response: QueryProcessorResponse = chain.invoke({"user_query": query})
    backend_logger.success("Query processed successfully")
    return QueryProcessorResponse(original_query=query, summary=response.summary)
