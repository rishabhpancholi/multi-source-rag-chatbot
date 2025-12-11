# Imports
from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi import APIRouter,HTTPException

from langchain_community.document_loaders import GithubFileLoader

from api.backend import create_knowledge,app_config

# Initialize router
codebase_knowledge_router = APIRouter()

# Input model
class CodebaseKnowledgeInput(BaseModel):
    session_id: str
    repo_name: str
    repo_branch: str

# Codebase knowledge route
@codebase_knowledge_router.post("/codebase_knowledge")
def create_codebase_knowledge(input: CodebaseKnowledgeInput)-> JSONResponse:
    try:
        js_loader = GithubFileLoader(
            repo = input.repo_name,
            branch = input.repo_branch,
            access_token = app_config.github_personal_access_token,
            github_api_url = app_config.github_api_url,
            file_filter = lambda file_path: file_path.endswith(".js")
        )
        python_loader = GithubFileLoader(
            repo = input.repo_name,
            branch = input.repo_branch,
            access_token = app_config.github_personal_access_token,
            github_api_url = app_config.github_api_url,
            file_filter = lambda file_path: file_path.endswith(".py")
        )
        markdown_loader = GithubFileLoader(
            repo = input.repo_name,
            branch = input.repo_branch,
            access_token = app_config.github_personal_access_token,
            github_api_url = app_config.github_api_url,
            file_filter = lambda file_path: file_path.endswith(".md")
        )
        js_docs = js_loader.load()
        python_docs = python_loader.load()
        markdown_docs = markdown_loader.load()
        
        if js_docs:
            create_knowledge(js_docs, input.session_id, type = "js")
        if python_docs:
            create_knowledge(python_docs, input.session_id, type = "python")
        if markdown_docs:
            create_knowledge(markdown_docs, input.session_id, type = "markdown")

        return JSONResponse({"message": "Codebase knowledge created successfully"})
    except HTTPException:
        raise 
    except Exception:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")