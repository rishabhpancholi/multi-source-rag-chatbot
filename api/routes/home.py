# Imports
from fastapi.responses import JSONResponse
from fastapi import APIRouter,HTTPException

# Initialize router
home_router = APIRouter()

# Home route
@home_router.get("/")
def home()-> JSONResponse:
    try:
        return JSONResponse({"message": "Welcome to the Multi Source RAG Chatbot!"})
    except Exception:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")