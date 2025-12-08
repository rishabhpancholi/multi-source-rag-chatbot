# Imports
from typing import TypedDict,Annotated

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage,AIMessage,SystemMessage
from langchain_core.output_parsers import StrOutputParser

from langgraph.graph.message import add_messages

from .config import app_config


# Chat model
llm =  ChatGroq(
    model = "llama-3.1-8b-instant",
    api_key = app_config.groq_api_key
)

# Chat state 
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    session_id: str

# Chat node
def chat_node(state: ChatState)-> ChatState:
    system_prompt = SystemMessage(
        content = """
          You are a helpful assistant.
          You are a multi source RAG chatbot.
          If user asks query which requires 
          retrieval from a knowledge base, 
          you can use the tools provided to you 
          to retrieve the knowledge.
          If the query doesnt require retrieval,
          just answer normally without retrieval.
          If even after retrieval you are not sure
          you can say i dont know. Do not make up 
          answers on yourself.
    """
    )
    messages = [system_prompt] + state["messages"]
    chat_model = llm | StrOutputParser()
    response = chat_model.invoke(
        messages
    )
    return {
        "messages": [AIMessage(content = response)],
        "session_id": state["session_id"]
    }
