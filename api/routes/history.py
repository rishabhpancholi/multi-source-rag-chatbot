# Imports
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from langchain_core.messages import HumanMessage,AIMessage

from api.backend import chatbot

# Initialize router
history_router = APIRouter()

# Chat history route
@history_router.get("/history/{session_id}")
def get_history(session_id: str)-> JSONResponse:
    try:
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        history = chatbot.get_state(config)
        messages = history.values["messages"]

        message_list = []
        for message in messages:
            if isinstance(message, AIMessage):
                message_list.append(
                    {"role": "assistant", "content": message.content}
                )
            elif isinstance(message, HumanMessage):
                message_list.append(
                    {"role": "human", "content": message.content}
                )

        return JSONResponse({"history": message_list})
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"{str(e)}")
