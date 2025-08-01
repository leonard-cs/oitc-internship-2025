from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.base import RunnableSerializable
from langchain_ollama import ChatOllama

from app.agent.models import AgentResponse
from app.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, backend_logger
from app.agent.tools import tools

ollama = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
)

system_prompt = """You are a helpful assistant that answers questions.
    When answering, use one of the tools provided. After using a tool the tool output will be provided in the 'scratchpad' below.
    If you have an answer in the scratchpad you should not use any more tools and instead answer directly to the user.
    Your responses should be concise and directly address the user's query.
    If you don't have enough information to answer the question, respond with "I don't know."
    """

prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template("{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

name2tool = {tool.name: tool.func for tool in tools}


class CustomAgentExecutor:
    chat_history: list[BaseMessage]

    def __init__(self, max_iterations: int = 3):
        # self.chat_history = []
        self.max_iterations = max_iterations
        self.agent: RunnableSerializable = (
            {
                "query": lambda x: x["query"],
                "agent_scratchpad": lambda x: x.get("agent_scratchpad", []),
            }
            | prompt_template
            | ollama.bind_tools(tools, tool_choice="any")
        )

    def invoke(self, query: str) -> AgentResponse:
        backend_logger.info("Invoking custom agent executor")
        count = 0
        agent_scratchpad = []
        while count < self.max_iterations:
            # invoke a step for the agent to generate a tool call
            tool_call = self.agent.invoke(
                {
                    "query": query,
                    # "chat_history": self.chat_history,
                    "agent_scratchpad": agent_scratchpad,
                }
            )
            backend_logger.trace(f"Reasoning: {tool_call.content}")

            # add initial tool call to scratchpad
            agent_scratchpad.append(tool_call)

            # otherwise we execute the tool and add it's output to the agent scratchpad
            tool_name = tool_call.tool_calls[0]["name"]
            tool_args = tool_call.tool_calls[0]["args"]
            tool_call_id = tool_call.tool_calls[0]["id"]
            tool_out = name2tool[tool_name](**tool_args)

            # add the tool output to the agent scratchpad
            tool_exec = ToolMessage(content=f"{tool_out}", tool_call_id=tool_call_id)
            agent_scratchpad.append(tool_exec)

            backend_logger.debug(f"Iteration {count + 1}: {tool_name}({tool_args})")
            count += 1
            # if the tool call is the final answer tool, we stop
            if tool_name == "final_answer":
                break
        # add the final output to the chat history
        # final_answer = tool_out.answer
        # self.chat_history.extend(
        #     [HumanMessage(content=query), AIMessage(content=final_answer)]
        # )
        # return the final answer in dict form
        backend_logger.success("Agent execution completed successfully")
        return tool_out
