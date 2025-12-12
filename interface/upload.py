# Imports
import time
import requests
import streamlit as st

# Upload File
def upload_file():
    file = st.sidebar.file_uploader(
        label = "Upload your file here",
        type=["pdf", "csv", "docx"]
    )

    submitted = st.sidebar.button("Upload")
    
    if submitted:
        if file is None:
            st.sidebar.warning("Please upload a file.")
        else:
            progress_bar = st.sidebar.progress(0, text = "Generating knowledge from file...")
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1, text = "Generating knowledge from file...")

            try:
                response = requests.post(
                    "http://localhost:8000/file_knowledge",
                    params = {
                        "session_id": st.session_state["session_id"],
                    },
                    files = {
                        "file": (file.name, file.getvalue(), file.type)
                    }
                )

                if response.status_code == 415:
                    st.sidebar.error("Invalid file type. Please upload a PDF, CSV, DOCX file.")
                elif response.status_code != 200:
                    st.sidebar.error("Error creating file knowledge. Please try again later.")
                else:
                    st.sidebar.success("File knowledge created successfully!")
            except Exception:
                st.sidebar.error("Error creating file knowledge. Please try again later.")

