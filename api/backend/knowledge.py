# Imports
from langsmith import traceable

from langchain_core.documents import Document
from langchain_voyageai.embeddings import VoyageAIEmbeddings
from langchain_qdrant.qdrant import QdrantVectorStore, QdrantVectorStoreError
from langchain_text_splitters.character import RecursiveCharacterTextSplitter, Language

from .config import app_config

# PDF knowledge
@traceable(name = "agentic_rag_chatbot")
def create_knowledge(docs: list[Document], session_id: str, type: str)-> None:
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language = Language.PYTHON,
            chunk_size = 500,
            chunk_overlap = 50
        )
        markdown_splitter = RecursiveCharacterTextSplitter.from_language(
            language = Language.MARKDOWN,
            chunk_size = 500,
            chunk_overlap = 50
        )
        js_splitter = RecursiveCharacterTextSplitter.from_language(
            language = Language.JS,
            chunk_size = 500,
            chunk_overlap = 50
        )
        splitter_dict = {
            "js": js_splitter,
            "python": python_splitter,
            "markdown": markdown_splitter,
            "text": text_splitter
        }

        chunks = splitter_dict[type].split_documents(docs)

        embeddings = VoyageAIEmbeddings(
            api_key = app_config.voyage_api_key,
            model = "voyage-3-large"
        )

        QdrantVectorStore.from_documents(
            documents = chunks,
            embedding = embeddings,
            collection_name = session_id,
            url = app_config.qdrant_url,
            api_key = app_config.qdrant_api_key
        )
    except QdrantVectorStoreError as e:
        raise Exception(f"Error creating knowledge: {str(e)}")

