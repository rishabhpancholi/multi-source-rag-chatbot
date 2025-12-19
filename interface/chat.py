# Imports
import json
import time
import requests
import streamlit as st

from upload import upload_file
from codebase import codebase_knowledge

# Chat interface
def chat()-> None:
    upload_file()
    codebase_knowledge()

    for message in st.session_state["previous_session_messages"]:
        if message["content"]:
            with st.chat_message(name = message["role"]):
                st.markdown(message["content"], unsafe_allow_html = True)
        else:
            st.status(label = "Using retrieval tool", state = "complete")

    for message in st.session_state["messages"]:
        with st.chat_message(name = message["role"]):
            st.markdown(message["content"], unsafe_allow_html = True)

    query = st.chat_input("Ask a question")
    if query:
        with st.chat_message(name = "human"):
            st.markdown(query, unsafe_allow_html = True)
        with st.spinner("Generating response..."):
            response_stream = requests.post(
                        url = f"{st.session_state['backend_url']}/respond",
                        json = {
                            "query": query,
                            "session_id": st.session_state["session_id"]
                        }
                )
        if response_stream.status_code != 200:
            st.error("Error fetching response. Please try again later.")
        else:
            for raw_json in response_stream.iter_lines(decode_unicode = True):
                if not raw_json:
                    continue
                
                try:
                    message = json.loads(raw_json)
                except json.JSONDecodeError:
                    continue

                tool_status_placeholder = st.empty()

                if message["type"] == "tool_call":
                    tool_status_placeholder.status(label = f"{message["message"]}", state = "complete")
                    time.sleep(0.1)
                if message["type"] == "tool_call_completed":
                    tool_status_placeholder.status(f"{message["message"]}", state = "complete")
                    time.sleep(0.1)
                if message["type"] == "response":

                    st.session_state["messages"].extend(
                        [
                            {"role": "human", "content": query},
                            {"role": "assistant", "content": message["message"]}
                        ]
                    )
                
                    with st.chat_message("assistant"):
                        placeholder = st.empty()
                        streamed_text = ""
                    
                        for chunk in message["message"].split(" "):
                            streamed_text += chunk + " "
                            placeholder.markdown(streamed_text, unsafe_allow_html = True)
                            time.sleep(0.03)

            

