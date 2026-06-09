from typing import TypedDict, List , Union
from langchain_core.messages import HumanMessage , AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # fast and free
    api_key=os.getenv("GROQ_API_KEY")
  
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))  # 👈 save response
    print(f"\nAI: {response.content}")
    print(f"Current State: {state['messages']}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []

User_input = input("Enter: ")
while User_input != "exit":
    conversation_history.append(HumanMessage(content=User_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]  # Update conversation history with the latest messages
    User_input = input("Enter: ")


with open("conversation_history.txt", "w") as file:
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"you: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n")
    file.write("\n--- End of Conversation ---\n")

print("Conversation history saved to conversation_history.txt")