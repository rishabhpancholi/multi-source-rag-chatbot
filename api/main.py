# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import (
    home_router,
    response_router,
    history_router,
    knowledge_router,
    codebase_knowledge_router
)

# Initialize app
app = FastAPI()

# Include routes
routes = [
    home_router,
    response_router,
    history_router,
    knowledge_router,
    codebase_knowledge_router
]
for route in routes:
    app.include_router(route)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)