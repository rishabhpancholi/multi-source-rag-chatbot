# Imports
import requests
import streamlit as st

# Get chat history
def get_chat_history(session_id: str)-> list[dict]:
    response = requests.get(f"{st.session_state['backend_url']}/history/{session_id}")

    if response.status_code == 200:
        messages = response.json()["history"]
        return messages
    else:
        return []