# Imports
import time
import requests
import streamlit as st

# Mention repo name and branch
def codebase_knowledge():
    with st.sidebar.form("codebase knowledge form"):
        st.write("Mention the repo name and branch")
        repo_name = st.text_input("Repo Name", key="repo_name")
        repo_branch = st.text_input("Branch Name", key="repo_branch")

        submitted = st.form_submit_button("Submit")
    if submitted:
            progress_bar = st.sidebar.progress(0, text = "Generating knowledge from file...")
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1, text = "Generating knowledge from file...")
            try:
                response = requests.post(
                    "http://localhost:8000/codebase_knowledge",
                    json = {
                        "repo_name": repo_name,
                        "repo_branch": repo_branch,
                        "session_id": st.session_state["session_id"]
                    }
                )
                if response.status_code != 200:
                    st.sidebar.error("Error creating codebase knowledge. Please try again later.")
                else:
                    st.sidebar.success("Codebase knowledge created successfully!")
            except Exception:
                st.sidebar.error("Error creating codebase knowledge. Please try again later.")   