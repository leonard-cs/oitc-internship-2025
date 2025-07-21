from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("./playground/.env"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="http://localhost:11500")
PHI3 = os.getenv("PHI3", default="phi3")


# Simplified schema for generating embedding-friendly structured text
class SemanticQuery(BaseModel):
    original_query: str = Field(description="The original user query")
    summary: str = Field(
        description="A concise summary of the query, capturing its essence"
    )
    # keywords: list[str] = Field(
    #     description="Key concepts or terms extracted from the query"
    # )


ollama = ChatOllama(
    model=PHI3,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
)
structured_ollama = ollama.with_structured_output(SemanticQuery)


def extract_semantic_query(user_query: str) -> SemanticQuery:
    # system_prompt = SystemMessagePromptTemplate.from_template(
    #     "You are an intelligent system that filters user input to extract only the meaningful, search-relevant information. "
    #     "Ignore casual greetings, emotions, and irrelevant small talk. Focus only on the part of the query that reflects a user's real informational or business intent."
    #     "Do not rephrase too much.\n\n"
    #     "Your goal is to:\n"
    #     "1. Identify the core topic or intent of the query.\n"
    #     "2. Generate a brief summary of that specific part only.\n"
    #     "3. Focus on products related query"
    #     "Only include the part of the user message that contains actionable or meaningful content. Do not mention pleasantries, greetings, or off-topic remarks in the output."
    # )
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
    # print(user_prompt.format(user_query=user_query))
    prompt = ChatPromptTemplate.from_messages([system_prompt, few_shot_prompt, user_prompt])
    # print(prompt.format(user_query=user_query))
    chain = {"user_query": RunnablePassthrough()} | prompt | structured_ollama
    msg = chain.invoke({"user_query": user_query})
    return msg


if __name__ == "__main__":
    extracted = extract_semantic_query(
        "The weather today is really nice. How are you? What is the most profitable product in our company?"
    )
    print(extracted)
