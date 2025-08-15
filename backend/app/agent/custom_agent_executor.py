from app.agent.models import AgentResponse
from app.agent.tools import tools
from app.agent.utils import remove_thinking_tags
from app.config import backend_logger
from app.llm.ollama import get_ollama
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.base import RunnableSerializable

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

    def __init__(self, max_iterations: int = 10):
        # self.chat_history = []
        self.max_iterations = max_iterations
        self.agent: RunnableSerializable = (
            {
                "query": lambda x: x["query"],
                "agent_scratchpad": lambda x: x.get("agent_scratchpad", []),
            }
            | prompt_template
            | get_ollama().bind_tools(tools, tool_choice="any")
        )

    def invoke(self, query: str) -> AgentResponse:
        backend_logger.info("Invoking custom agent executor")
        count = 1
        agent_scratchpad = []
        while True:
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

            # check if there are any tool calls
            if not tool_call.tool_calls:
                backend_logger.warning(
                    "No tool calls generated, returning content as final answer"
                )
                # If no tool calls, return the content as a final answer
                return AgentResponse(
                    answer=remove_thinking_tags(tool_call.content) or "I don't know.",
                    sources=[],
                    tools_used=[],
                )

            # otherwise we execute the tool and add it's output to the agent scratchpad
            tool_name = tool_call.tool_calls[0]["name"]
            tool_args = tool_call.tool_calls[0]["args"]
            tool_call_id = tool_call.tool_calls[0]["id"]
            backend_logger.debug(f"Iteration {count}: {tool_name}({tool_args})")
            tool_out = name2tool[tool_name](**tool_args)

            # add the tool output to the agent scratchpad
            tool_exec = ToolMessage(content=f"{tool_out}", tool_call_id=tool_call_id)
            agent_scratchpad.append(tool_exec)

            # if the tool call is the final answer tool, we stop
            if tool_name == "final_answer":
                break
            if count >= self.max_iterations:
                backend_logger.warning(
                    "Max iterations reached, returning content as final answer"
                )
                return AgentResponse(
                    answer=remove_thinking_tags(tool_call.content)
                    or "Max agent iterations reached.",
                    sources=[],
                    tools_used=[],
                )

            count += 1
        # add the final output to the chat history
        # final_answer = tool_out.answer
        # self.chat_history.extend(
        #     [HumanMessage(content=query), AIMessage(content=final_answer)]
        # )
        # return the final answer in dict form
        backend_logger.success("Agent execution completed successfully")
        return tool_out
