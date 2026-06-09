from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
from operator import add as add_messages
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # 👈 much better at tool use
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"  # runs locally, no API key needed
)

pdf_path = "/workspaces/Agentic-AI/Agents/Stock_Market_Performance_2024.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)

try:
    pages = pdf_loader.load()
except Exception as e:
    print(f"Error loading PDF: {str(e)}")
    raise

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
      )

persist_directory = "pdf_chunks"
collection_name = "stock_market_performance"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    # Split the loaded PDF pages into chunks for the vector store
    pages_split = text_splitter.split_documents(pages)

    try:
        vector_store = Chroma.from_documents(
            documents=pages_split,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        print("Vector store created successfully.")

    except Exception as e_inner:
        err_str = str(e_inner)
        # If the collection/database already exists, try to load the existing DB instead of recreating it.
        if 'table collections already exists' in err_str or 'already exists' in err_str:
            print("Existing Chroma DB detected — attempting to load existing vector store.")
            try:
                # Load existing Chroma vector store from the persist directory.
                vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
                print("Loaded existing vector store.")
            except Exception as e_load:
                print(f"Failed to load existing vector store: {e_load}")
                raise
        else:
            print(f"Error creating vector store: {err_str}")
            raise

except Exception as e:
    print(f"Error creating vector store: {str(e)}")
    raise

retriever = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 5}
)

@tool
def retriever_tool(query: str) -> str:
    """
    This tool searches and returns information from the Stock Market Performance 2024 document.
    """
    # Use the retriever to get relevant documents
    try:
        # Depending on LangChain version the method may be `get_relevant_documents` or `retrieve`.
        if hasattr(retriever, "get_relevant_documents"):
            docs = retriever.get_relevant_documents(query)
        elif hasattr(retriever, "retrieve"):
            docs = retriever.retrieve(query)
        else:
            # Fallback to invoking if the retriever is wrapped
            docs = retriever.invoke(query)
    except Exception as e:
        return f"Error querying retriever: {e}"

    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 document."

    results = []
    for i, doc in enumerate(docs):
        # Some retriever document objects store text in `page_content` or `text`
        content = getattr(doc, "page_content", None) or getattr(doc, "text", str(doc))
        results.append(f"Document {i+1}:\n{content}")

    return "\n\n".join(results)

tools = [retriever_tool]

llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState) -> str:
    """Check if the last message contains tool calls."""
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""
tools_dict = {t.name: t for t in tools} # Creating a dictionary of our tools

def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state."""
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {'messages': [message]}

def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""

    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        
        if not t['name'] in tools_dict: # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
            

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {True: "retriever_agent", False: END}
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


def running_agent():
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})
        
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()