# Imports
import requests
import streamlit as st

from upload import upload_file
from codebase import codebase_knowledge

# Chat interface
def chat()-> None:
    upload_file()
    codebase_knowledge()

    for message in st.session_state["previous_session_messages"]:
        with st.chat_message(name = message["role"]):
            st.markdown(message["content"])

    for message in st.session_state["messages"]:
        with st.chat_message(name = message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask a question")
    if query:
        with st.chat_message(name = "human"):
            st.markdown(query)
        with st.spinner("Generating response..."):
            response = requests.post(
                        url = "http://localhost:8000/respond",
                        json = {
                            "query": query,
                            "session_id": st.session_state["session_id"]
                        }
                )
        if response.status_code != 200:
            st.error("Error fetching response. Please try again later.")
        else:
            response_msg = response.json()["response"]
            st.session_state["messages"].extend(
                [
                    {"role": "human", "content": query},
                    {"role": "assistant", "content": response_msg}
                ]
            )
            with st.chat_message(name = "assistant"):
                st.markdown(response_msg)
               

            

