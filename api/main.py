# Imports
from fastapi import FastAPI

from api.routes import (
    home_router,
    response_router,
    history_router,
    knowledge_router
)

# Initialize app
app = FastAPI()

# Include routes
routes = [
    home_router,
    response_router,
    history_router,
    knowledge_router
]
for route in routes:
    app.include_router(route)