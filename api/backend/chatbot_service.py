# Imports
import psycopg

from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.postgres import PostgresSaver

from .config import app_config
from .retrieval_node import tool_node
from .chat_node import ChatState,chat_node

# Postgres connection
conn = psycopg.connect(f"postgresql://{app_config.postgres_user}:{app_config.postgres_password}@postgres_db:5432/{app_config.postgres_db}", autocommit = True)

# Initialize Checkpointer
checkpointer = PostgresSaver(conn = conn)
checkpointer.setup()

# Chatbot graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges(
    "chat_node",
    tools_condition,
    {
        "tools": "tool_node",
        "__end__": END
    }
)
graph.add_edge("tool_node", "chat_node")
chatbot = graph.compile(
    checkpointer = checkpointer
)
