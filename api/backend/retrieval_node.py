# Imports
from langchain_core.tools import tool
from langchain_voyageai.embeddings import VoyageAIEmbeddings
from langchain_qdrant.qdrant import QdrantVectorStore, QdrantVectorStoreError

from langgraph.prebuilt import ToolNode

from .config import app_config

@tool("retriever")
def retrieval_tool(query: str, session_id: str) -> str:
    """
    Takes user query ('query') and chat session id ('session_id') as input and returns context as a string after retrieving data from Qdrant vector store.

    Args:
       query: User's query string
       session_id: Chat session id string
    """
    embeddings = VoyageAIEmbeddings(
        api_key = app_config.voyage_api_key,
        model = "voyage-3-large"
    )

    try:
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=session_id,
            url="http://localhost:6333"
        )

        relevant_docs = vector_store.similarity_search(query, k = 3)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        return context

    except QdrantVectorStoreError as e:
        return f"Error retrieving data from vector store: {str(e)}"

tool_node = ToolNode(tools = [retrieval_tool])