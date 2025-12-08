# Imports
import psycopg
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgresSaver

from .config import app_config
from .chat_node import ChatState,chat_node

# Postgres connection
conn = psycopg.connect(f"postgresql://{app_config.postgres_user}:{app_config.postgres_password}@localhost:5432/{app_config.postgres_db}", autocommit = True)

# Initialize Checkpointer
checkpointer = PostgresSaver(conn = conn)
checkpointer.setup()

# Chatbot graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(
    checkpointer = checkpointer
)
