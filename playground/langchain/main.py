from config import OLLAMA_BASE_URL, PHI3
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM

ollama = OllamaLLM(model=PHI3, base_url=OLLAMA_BASE_URL)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant that answers questions based only on the provided context."
            " If you don't know the answer, say you don't know. Keep the answer concise.",
        ),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ]
)
# prompt.pretty_print()

question = "Why is sky blue?"
context = "The sky appears blue because of the scattering of light by the atmosphere."

prompt.invoke({"context": context, "question": question})

chain = (
    {
        "context": RunnablePassthrough(),
        "question": RunnablePassthrough(),
    }
    | prompt
    | ollama
    | StrOutputParser()
)
print(chain.invoke({"context": context, "question": question}))
