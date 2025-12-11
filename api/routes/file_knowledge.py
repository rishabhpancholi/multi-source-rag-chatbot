# Imports
import tempfile

from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, HTTPException, File

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
    UnstructuredExcelLoader
)

from api.backend import create_knowledge

# Initialize router
knowledge_router = APIRouter()

LOADERS = {
    "pdf": PyPDFLoader,
    "csv": CSVLoader,
    "docx": Docx2txtLoader,
    "xlsx": UnstructuredExcelLoader
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
            docs = loader.load()

            create_knowledge(docs, session_id, type = "text")

        return JSONResponse({"message": "File knowledge created successfully"})

    except HTTPException:
        raise 
    except Exception:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")