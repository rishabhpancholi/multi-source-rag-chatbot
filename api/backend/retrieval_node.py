# Imports
from langchain_core.tools import tool
from langchain_voyageai.embeddings import VoyageAIEmbeddings
from langchain_qdrant.qdrant import QdrantVectorStore, QdrantVectorStoreError

from langgraph.prebuilt import ToolNode

from .config import app_config

@tool("retriever", description="A tool which retrieves data from a vector store and returns context as a string.")
def retrieval_tool(query: str, session_id: str) -> str:
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

        relevant_docs = vector_store.similarity_search(query)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        return context

    except QdrantVectorStoreError as e:
        return f"Error retrieving data from vector store: {str(e)}"

tool_node = ToolNode(tools = [retrieval_tool])