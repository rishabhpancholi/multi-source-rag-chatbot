# Imports
import tempfile

from langsmith import tracing_context

from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, HTTPException, File

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
)
from langchain_core.runnables import RunnableLambda

from api.backend import create_knowledge,langsmith_client

# Initialize router
knowledge_router = APIRouter()

LOADERS = {
    "pdf": PyPDFLoader,
    "csv": CSVLoader,
    "docx": Docx2txtLoader
}

# Knowledge route
@knowledge_router.post("/file_knowledge")
async def create_file_knowledge(session_id: str, file: UploadFile = File(...))-> JSONResponse:
    try:
        file_extension = file.filename.split(".")[-1].lower() 
        if file_extension not in LOADERS.keys():
            raise HTTPException(status_code = 415, detail = "Invalid file type")
        
        with tempfile.NamedTemporaryFile(delete = False, suffix = file_extension) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

            loader = LOADERS[file_extension](tmp_path)

        config = {
            "run_name": "agentic-rag-chatbot"
        }

        with tracing_context(
            enabled = True,
            client = langsmith_client,
            project_name = "agentic-rag-chatbot",
            metadata = {"thread_id": session_id}
        ):
            load_docs = RunnableLambda(lambda _: loader.load())
            docs = load_docs.invoke(None, config = config)
            create_knowledge(docs, session_id, type = "text")

        return JSONResponse({"message": "File knowledge created successfully"})

    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"{str(e)}")