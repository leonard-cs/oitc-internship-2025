from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("/playground/.env"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", default="http://localhost:11500")
PHI3 = os.getenv("PHI3", default="phi3")


class Result(BaseModel):
    generated_summary: str = Field(description="The summary generated by the model.")
    judgment: bool = Field(
        description="Evaluation judgment: 'true' if the summary is accurate, 'false' if it is misleading or wrong."
    )
    explanation: str = Field(
        description="Explanation of the evaluation judgment, why the summary is considered accurate or misleading."
    )


def evaluate_summary_with_llm(
    reference_summary: str,
    generated_summary: str,
) -> Result:
    """
    Uses an LLM to evaluate whether the generated summary is accurate and complete
    compared to the original query and the reference summary.

    Returns: Evaluation judgment as a string ("Correct", "Partially correct", "Incorrect")
    """
    system_prompt = SystemMessagePromptTemplate.from_template(
        "You are an expert evaluator that compares a generated summary to a reference summary. "
        "Your task is to determine whether the generated summary semantically matches the reference.\n\n"
        "Return strictly one of the following:\n"
        "- true: if the summary is accurate and complete (semantically equivalent).\n"
        "- false: if the summary is incorrect, incomplete, or changes the meaning.\n\n"
        "Do not explain your answer. Only return true or false."
    )
    user_prompt = HumanMessagePromptTemplate.from_template(
        """Reference Summary:\n{reference_summary}\n\n
           Generated Summary:\n{generated_summary}\n\n
           Are the meanings similar?""",
        input_variables=["reference_summary", "generated_summary"],
    )
    # print(user_prompt.format(
    #     reference_summary=reference_summary,
    #     generated_summary=generated_summary,
    # ))

    evaluation_prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])
    # print(evaluation_prompt.format(
    #     reference_summary=reference_summary,
    #     generated_summary=generated_summary,
    # ))
    evaluation_llm = ChatOllama(
        model=PHI3, base_url=OLLAMA_BASE_URL
    ).with_structured_output(Result)
    chain = (
        {
            "reference_summary": RunnablePassthrough(),
            "generated_summary": RunnablePassthrough(),
        }
        | evaluation_prompt
        | evaluation_llm
    )
    response = chain.invoke(
        {
            "reference_summary": reference_summary,
            "generated_summary": generated_summary,
        }
    )

    return response


if __name__ == "__main__":
    result = evaluate_summary_with_llm(
        reference_summary="Most profitable product query",
        generated_summary="Most profitable product query",
    )
    print(result)
