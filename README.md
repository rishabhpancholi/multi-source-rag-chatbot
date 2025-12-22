# 🧠 Multi-Source RAG Chatbot

A **production-ready, multi-source Retrieval-Augmented Generation (RAG) chatbot** built using **LangChain**, **LangGraph**, and **FastAPI**.

The system supports **document ingestion**, **GitHub codebase ingestion**, **session-based chat history**, **streaming responses**, **observability**, and access via both **API and Streamlit UI**.

This project is designed to be **extensible, debuggable, and deployable**.

---

## 🚀 Key Features

- **Multi-source RAG** (Documents: PDF, DOCX, CSV + GitHub repositories)
- **LangGraph-powered agent workflow**
- **Qdrant** for vector storage, semantic search, and retrieval
- **PostgreSQL** for persistence (chat history, sessions, metadata)
- **FastAPI** backend with streaming support
- **LangSmith** integration for observability and tracing
- **Session-based memory**
- **File ingestion** (PDF, DOCX, CSV)
- **GitHub codebase ingestion** (repository + branch)

---

## 🧠 LangGraph Workflow

The agent graph consists of two primary nodes:

### 1️⃣ Chat Node

- Maintains the **session ID**
- Handles user messages
- Decides whether a **tool call** is required

### 2️⃣ Tool Node (Retriever)

- Fetches relevant context from **Qdrant** using semantic search

### Workflow Execution

- The user message list along with the session ID enters the **Chat Node**
- The Chat Node generates an `AIMessage`
- `tools_condition` determines whether:

  - the workflow ends, or
  - control is passed to the **Tool Node**

- The Tool Node generates a `ToolMessage` and returns it to the Chat Node
- The Chat Node produces the final human-readable response

---

## 🛠️ Tech Stack

| Layer               | Technology              |
| ------------------- | ----------------------- |
| LLM Orchestration   | LangChain, LangGraph    |
| Backend API         | FastAPI                 |
| Vector Database     | Qdrant                  |
| Relational Database | PostgreSQL              |
| Observability       | LangSmith               |
| UI                  | Streamlit               |
| Containerization    | Docker & Docker Compose |

---

## 📡 API Endpoints Overview

The backend is exposed as a **REST + streaming API** using **Server-Sent Events (SSE)**, making it usable both via the UI and directly in other applications.

### Core Capabilities

- Streaming chat responses
- Session-based conversation history
- File-based knowledge ingestion
- GitHub repository knowledge ingestion
- Observability via LangSmith traces

---

### 🔹 `POST /respond`

- Sends a user query to the chatbot
- Returns streaming response events (`application/x-ndjson`)
- Requires a **session ID**

---

### 🔹 `GET /history/{session_id}`

- Retrieves the full conversation history for a given session ID

---

### 🔹 `POST /file_knowledge`

- Requires a session ID
- Supports file uploads:

  - PDF
  - DOCX
  - CSV

- Files are chunked, embedded, and stored in **Qdrant**

---

### 🔹 `POST /codebase_knowledge`

- Loads Python, JavaScript, and Markdown files from a GitHub repository
- Converts the codebase into embeddings stored in **Qdrant**
- Required inputs:

  - `repo_name`
  - `repo_branch`

---

## ▶️ How to Run the API Locally (Docker)

### Prerequisites

- Docker
- Docker Compose

---

### Steps

1. Clone the repository
2. Create a `.env` file and copy variables from `.env-demo`
3. Fill in your own API keys and PostgreSQL credentials

---

### Option 1: Pull Image from Docker Hub

```bash
docker pull rishabhpancholi/agentic-rag-chatbot:latest
docker compose up -d
```

---

### Option 2: Build & Run via Docker Compose

```bash
docker compose up -d
```

Docker Compose will build or pull the image and start all required services.

---

### Access the Application

- API Base URL: `http://localhost:8000`
- API Docs (Swagger): `http://localhost:8000/docs`

---

### Stop and Clean Containers

```bash
docker compose down -v
```

> ⚠️ This removes volumes and clears persisted data.

---

## 🎨 Streamlit UI

For a UI-based chat experience:

1. Create and activate a Python virtual environment
2. Install Streamlit
3. Run the UI:

```bash
streamlit run interface/main.py --server.port 8502
```

- UI will be available at: `http://localhost:8502`

---

## 🔌 Using as an API in Your Own App

You can integrate this chatbot into:

- Web applications
- Internal tools
- Other agent systems

Simply call the exposed **FastAPI endpoints**.

---

## 🧩 Extensibility Notes

You can easily extend this system by:

- Adding new tools to LangGraph
- Supporting additional file types
- Introducing multi-agent workflows
- Adding authentication and rate limiting

---

## 🤝 Contributing

Contributions, suggestions, and critiques are welcome.

**Contact**

- Email: [rishabhpancholi134@gmail.com](mailto:rishabhpancholi134@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/rishabh-pancholi-9a31b9191/](https://www.linkedin.com/in/rishabh-pancholi-9a31b9191/)
