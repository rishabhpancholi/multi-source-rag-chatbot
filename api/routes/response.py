# Imports
import json

from pydantic import BaseModel

from langsmith import tracing_context

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from api.backend import chatbot,langsmith_client

# Input model
class ChatInput(BaseModel):
    query: str
    session_id: str

# Initialize router
response_router = APIRouter()

# Serialization code
def serialize_messages(chunk: dict)-> str:
    if "chat_node" in chunk:
        messages = chunk["chat_node"].get("messages", [])
        if not messages:
            return None
        msg_chunk = messages[0]
        if isinstance(msg_chunk, AIMessage) and msg_chunk.tool_calls:
            event = {
                "type": "tool_call",
                "message": f"Calling {msg_chunk.tool_calls[0]["name"]}"
            }
            return json.dumps(event) + "\n"
        
        if isinstance(msg_chunk, AIMessage) and msg_chunk.content:
            event = {
                "type": "response",
                "message": msg_chunk.content
            }
            return json.dumps(event) + "\n"
        
    if "tool_node" in chunk:
        tool_messages = chunk["tool_node"].get("messages", [])
        if not tool_messages:
            return None
        tool_msg = tool_messages[0]
        if isinstance(tool_msg, ToolMessage) and tool_msg.name:
            event = {
                "type": "tool_call_completed",
                "message": f"Called {tool_msg.name}"
            }
            return json.dumps(event) + "\n"

# Response route
@response_router.post("/respond")
def respond(input: ChatInput)-> StreamingResponse:
    try:
        def response_event():
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
                for chunk in chatbot.stream(
                    {
                        "session_id": input.session_id,
                        "messages": [HumanMessage(content = input.query)]
                    },
                    config = config,
                    stream_mode = "updates"
                ): 
                    serialized_chunk = serialize_messages(chunk)
                    if serialized_chunk is not None:
                        yield serialized_chunk

        return StreamingResponse(
            content = response_event(),
            media_type = "application/x-ndjson"
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"{str(e)}")
    