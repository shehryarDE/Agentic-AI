from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
import os  # 👈 was missing

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  # 👈 fixed annotation

@tool
def add(a: int, b: int):
    """Adds two numbers together."""
    return a + b

@tool  # 👈 was missing
def subtract(a: int, b: int):
    """Subtracts the second number from the first."""
    return a - b

@tool  # 👈 was missing
def multiply(a: int, b: int):
    """Multiplies two numbers together."""
    return a * b

tools = [add, subtract, multiply]  # 👈 list not set

model = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
).bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are a helpful assistant that can perform basic arithmetic operations using the provided tools.")
    response = model.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [response]}

def continue_state(state: AgentState) -> str:  # 👈 return type str
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return 'end'
    else:
        return 'continue'

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)  # 👈 no spaces in node name

tool_node = ToolNode(tools=tools)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "our_agent")

graph.add_conditional_edges(
    "our_agent", continue_state, {
        'continue': "tool_node",  # 👈 missing comma fixed
        'end': END,
    }
)

graph.add_edge("tool_node", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]  # 👈 'messages' not 'message'
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))