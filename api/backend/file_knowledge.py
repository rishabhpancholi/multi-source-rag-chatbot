# Imports
from langchain_core.documents import Document
from langchain_qdrant.qdrant import QdrantVectorStore
from langchain_voyageai.embeddings import VoyageAIEmbeddings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from .config import app_config

# PDF knowledge
def create_knowledge(docs: list[Document], session_id: str)-> None:
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        chunks = splitter.split_documents(docs)

        embeddings = VoyageAIEmbeddings(
            api_key = app_config.voyage_api_key,
            model = "voyage-3-large"
        )

        QdrantVectorStore.from_documents(
            documents = chunks,
            embedding = embeddings,
            collection_name = session_id,
            url = "http://localhost:6333"
        )
    except Exception as e:
        raise Exception(f"Error creating knowledge: {str(e)}")

