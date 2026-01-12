# YogaMantri – Wellness RAG Micro-App

YogaMantri is a full-stack AI micro-application that answers yoga and wellness-related questions using a Retrieval-Augmented Generation (RAG) pipeline. The system emphasizes safe, non-medical responses and clearly surfaces source context for transparency.

---

## Features

- RAG-based question answering using a custom yoga knowledge base
- Safety layer for sensitive queries (pregnancy, injuries, medical conditions)
- Source attribution for each response
- User feedback logging (helpful / not helpful)
- MongoDB-based query and feedback analytics
- Unified deployment (frontend + backend)
- Android APK (WebView-based)

---

## Tech Stack

### Frontend
- Next.js (React)
- Minimal UI for query input, response display, and feedback

### Backend
- FastAPI (Python)
- RAG pipeline for retrieval and generation
- Safety heuristics for risk-sensitive topics

### Database
- MongoDB Atlas
  - Stores user queries
  - Stores retrieved context
  - Stores feedback signals

### Vector Store
- ChromaDB local vector database (built from curated yoga documents)

---

## RAG Pipeline Overview

1. Source documents stored in `/sources`
2. Documents are chunked and embedded
3. Embeddings stored in a vector database
4. On user query:
   - Relevant chunks are retrieved
   - Context is injected into the prompt
   - Final response is generated using the model

The vector database is automatically initialized on first startup if empty.

---

## Safety Logic

Queries are flagged as unsafe if they mention:
- Pregnancy
- Recent surgery
- Injuries or medical conditions

For unsafe queries:
- A warning message is shown
- Only general, non-medical guidance is provided
- Users are advised to consult professionals

---

## API Endpoints

- `POST /ask` – Submit a yoga-related question
- `POST /feedback` – Submit helpful/not helpful feedback
- `POST /admin/rebuild-vec-db` – Admin endpoint to rebuild vector database
- `POST /admin/upload` - Upload PDF / DOCX / TXT and ingest into vector DB
- `POST /admin/reset` - Dangerous operation: clears entire vector store knowledge base
- `GET /admin/documents` - List all ingested documents in the vector DB
- `DELETE /admin/documents/{source_doc_id}` - Delete all chunks belonging to a specific document

---

## Deployment

The frontend is statically built and served directly by the FastAPI backend, allowing a single unified deployment URL.

- Backend + Frontend hosted on Render
- MongoDB hosted on MongoDB Atlas

---

## Android APK

The Android app is a WebView-based wrapper around the hosted web application, generated using Bubblewrap. The APK is fully functional and requires no local setup.

[click here to get the `.apk` file](https://drive.google.com/drive/folders/1fMLJnrV0lM5bA0cmiYm8V4fov1pq6jJg)

---

## How to Run Locally

### Environment Variables Setup (Required)

Before running the application, create a `.env` file inside the **root directory** with the following variables:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/
GROQ_API_KEY=your_openai_api_key_here
HF_API_TOKEN=your_huggingface_api_key_here
```

### Terminal Commands

```bash
pip install -r requirements.txt
cd frontend && npm install && npm run build
uvicorn backend.main:app --reload
```

### Notes
- Do not commit the .env file to GitHub.
- The vector database is automatically created from the /sources folder on first startup.
