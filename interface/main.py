# Imports
import streamlit as st

from chat import chat
from chat_history import get_chat_history

# Title
st.sidebar.title("Multi Source RAG Chatbot")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "session_id" not in st.session_state:
    st.session_state["session_id"]= None
if "previous_session_messages" not in st.session_state:
    st.session_state["previous_session_messages"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not st.session_state.logged_in:
    # Login form
    with st.form("login form"):
        st.write("Login with your username")
        username =st.text_input("Enter Your username", key="username")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["logged_in"] = True
            st.session_state["session_id"] = username
            with st.spinner("Loading chat history..."):
                st.session_state["previous_session_messages"] = get_chat_history(username)
            st.rerun()
else:
    chat()

