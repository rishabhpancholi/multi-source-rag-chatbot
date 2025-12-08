# Imports
from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from langchain_core.messages import HumanMessage

from api.backend import chatbot

# Input model
class ChatInput(BaseModel):
    query: str
    session_id: str

# Initialize router
response_router = APIRouter()

# Response route
@response_router.post("/respond")
def respond(input: ChatInput)-> JSONResponse:
    try:
        config = {
            "configurable": {
                "thread_id": input.session_id
            }
        }
        response = chatbot.invoke(
            {
                "session_id": input.session_id,
                "messages": [HumanMessage(content = input.query)]
            },
            config = config
        )

        return JSONResponse({"response": response["messages"][-1].content})
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"{str(e)}")