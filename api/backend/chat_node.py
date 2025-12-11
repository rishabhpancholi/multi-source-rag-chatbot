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
          If the query doesn't require retrieval,just answer normally without retrieval.
          If user asks query which requires retrieval of document string from 
          a knowledge base(vector database), you can use the tool `retrieval_tool` 
          provided to you to retrieve the knowledge.
          If even after retrieval you are not sure you can say i dont know. Do not make up 
          answers on yourself.
          The session_id for the chat is {state["session_id"]}.
          The `retrieval_tool` takes two fixed arguments "query" and "session_id".
          Inside query there will be the user's query.
          Inside session_id there will be the session_id for the chat.
          Strictly follow this while calling the tool otherwise tool call will fail!!!
          For example:
          The tool call will be like:
          ```
          retrieval_tool(query, session_id)
          ```
          You also have a search tool called the `search_tool`.
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
