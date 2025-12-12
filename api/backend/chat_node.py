# Imports
from typing import TypedDict,Annotated

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage,SystemMessage

from langgraph.graph.message import add_messages

from .config import app_config
from .retrieval_node import retrieval_tool


# Chat model
llm =  ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = app_config.groq_api_key
)

# Chat state 
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    session_id: str

# Chat node
def chat_node(state: ChatState)-> ChatState:
    system_prompt = SystemMessage(
        content = f"""
          You are a helpful assistant.
          You are a multi source RAG(Retrieval Augmented Generation) chatbot.
          Always give a short intro when user asks for it.
          You have access to a Qdrant vector database for retrieving knowledge through a
          tool called `retrieval_tool`. 
          When the user explicitly asks who/what you are, give a short intro.
          Use retrieval only when the user explicitly asks for knowledge from the stored documents, 
          or when the response requires factual details unlikely to be in your general model knowledge.
          If even after retrieval you are not sure you can just say 'I dont know'. Do not make up 
          answers by yourself.
          The session_id for the chat is {state["session_id"]}.
          Always call the tool with the correct arguments which are mentioned in the tool description.
          
    """
    )
    messages = [system_prompt] + state["messages"]
    rag_model = llm.bind_tools([retrieval_tool])
    response = rag_model.invoke(
        messages
    )
    return {
        "messages": [response],
        "session_id": state["session_id"]
    }
