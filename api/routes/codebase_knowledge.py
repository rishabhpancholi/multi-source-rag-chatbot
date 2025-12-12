# Imports
from pydantic import BaseModel

from langsmith import tracing_context

from fastapi.responses import JSONResponse
from fastapi import APIRouter,HTTPException

from langchain_core.runnables import RunnableLambda
from langchain_community.document_loaders import GithubFileLoader

from api.backend import create_knowledge,app_config,langsmith_client

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
        
        load_js_docs = RunnableLambda(lambda _: js_loader.load())
        load_python_docs = RunnableLambda(lambda _: python_loader.load())
        load_markdown_docs = RunnableLambda(lambda _: markdown_loader.load())

        config = {
            "run_name": "agentic-rag-chatbot"
        }
        
        with tracing_context(
            enabled = True,
            client = langsmith_client,
            project_name = "agentic-rag-chatbot",
            metadata = {"thread_id": input.session_id}
        ):
            js_docs = load_js_docs.invoke(None, config = config)
            python_docs = load_python_docs.invoke(None, config = config)
            markdown_docs = load_markdown_docs.invoke(None, config = config)

            if js_docs:
                create_knowledge(js_docs, input.session_id, type = "js")
            if python_docs:
                create_knowledge(python_docs, input.session_id, type = "python")
            if markdown_docs:
                create_knowledge(markdown_docs, input.session_id, type = "markdown")

        return JSONResponse({"message": "Codebase knowledge created successfully"})
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"{str(e)}")