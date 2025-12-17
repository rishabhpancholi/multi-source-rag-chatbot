# Imports
from pydantic import BaseModel

from langsmith import tracing_context

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from langchain_core.messages import HumanMessage, AIMessage

from api.backend import chatbot,langsmith_client

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
            },
            "metadata":{
                "thread_id": input.session_id
            },
            "run_name": "agentic-rag-chatbot"
        }

        with tracing_context(
            enabled = True,
            client = langsmith_client,
            project_name = "agentic-rag-chatbot"
        ):
            response = chatbot.invoke(
                {
                    "session_id": input.session_id,
                    "messages": [HumanMessage(content = input.query)]
                },
                config = config
            )

        response_messages = []

        messages = response["messages"]
        for message in messages:
            if isinstance(message, AIMessage):
                response_messages.append(
                    {
                        "role": "assistant",
                        "content": message.content
                    }
                )
                
        return JSONResponse({
            "response": response_messages
        })
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"{str(e)}")