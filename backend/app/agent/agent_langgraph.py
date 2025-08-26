import time

from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.config import get_stream_writer
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_MODEL = "qwen3:latest"


def visualize_graph(graph: CompiledStateGraph):
    png_graph = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_graph)

    ascii_graph = graph.get_graph().draw_ascii()
    with open("graph.txt", "w") as f:
        f.write(ascii_graph)


def add(x: int, y: int) -> int:
    """Add two numbers"""
    writer = get_stream_writer()
    writer(f"Adding {x} and {y}")
    return x + y


def sub(x: int, y: int) -> int:
    """Subtract two numbers"""
    writer = get_stream_writer()
    writer(f"Subtracting {x} and {y}")
    return x - y


def stream_agent_messages(agent: CompiledStateGraph, config: dict, input_message: dict):
    for step in agent.stream(
        {"messages": [input_message]}, config, stream_mode="values"
    ):
        step["messages"][-1].pretty_print()
        # print(step["messages"][-1].content)
        print()


def stream_agent_progress(agent: CompiledStateGraph, config: dict, input_message: dict):
    for chunk in agent.stream(
        {"messages": [input_message]}, config, stream_mode="updates"
    ):
        print(chunk)
        print("\n")


def stream_agent_tokens(agent: CompiledStateGraph, config: dict, input_message: dict):
    for token, metadata in agent.stream(
        {"messages": [input_message]}, config, stream_mode="messages"
    ):
        # print("Token", token)
        # print("Metadata", metadata)
        # print("\n")
        if metadata["langgraph_node"] == "agent" and (text := token.text()):
            print(text, end="|")
        time.sleep(0.01)  # Delay to simulate streaming


def stream_tool_updates(agent: CompiledStateGraph, config: dict, input_message: dict):
    for chunk in agent.stream(
        {"messages": [input_message]}, config, stream_mode=["custom"]
    ):
        print(chunk)
        print("\n")


def custom_streaming(agent: CompiledStateGraph, config: dict, input_message: dict):
    for stream_mode, chunk in agent.stream(
        {"messages": [input_message]}, config, stream_mode=["custom", "messages"]
    ):
        if stream_mode == "custom":
            print(f"<tool_call>\n{chunk}\n</tool_call>\n")
        if stream_mode == "messages":
            token, metadata = chunk
            if metadata["langgraph_node"] == "agent" and (text := token.text()):
                print(text, end="|")
            time.sleep(0.01)  # Delay to simulate streaming


def main():
    memory = MemorySaver()
    model = ChatOllama(model=OLLAMA_CHAT_MODEL, base_url=OLLAMA_BASE_URL)

    tools = [add]

    agent_executor = create_react_agent(model, tools, checkpointer=memory)
    # visualize_graph(agent_executor)
    config = {"configurable": {"thread_id": "abc123"}}

    input_message = {"role": "user", "content": "Hi, my name is John Doe."}
    stream_agent_messages(agent_executor, config, input_message)

    # input_message = {"role": "user", "content": "What is my name?"}
    # # stream_agent_progress(agent_executor, config, input_message)
    # stream_agent_tokens(agent_executor, config, input_message)

    input_message = {"role": "user", "content": "What is 1 + 1?"}
    # stream_tool_updates(agent_executor, config, input_message)
    custom_streaming(agent_executor, config, input_message)


if __name__ == "__main__":
    main()
