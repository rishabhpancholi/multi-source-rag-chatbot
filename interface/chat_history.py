# Imports
import requests

# Get chat history
def get_chat_history(session_id: str)-> list[dict]:
    response = requests.get(f"http://localhost:8000/history/{session_id}")

    if response.status_code == 200:
        messages = response.json()["history"]
        return messages
    else:
        return []