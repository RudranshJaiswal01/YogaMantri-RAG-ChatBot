import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.admin import router as admin_router
from backend.utils import is_query_unsafe
from backend.generation import generate_answer
from rag.rewrite import rewrite_query
from rag.retrieval import retrieve_chunks
from rag.embeddings import embed_texts
from rag.rebuild_internal import rebuild_vector_db_internal
from db.mongo_db import log_query, log_feedback
from db.vector_db import vector_store_is_empty

app = FastAPI(title="HR Knowledge Base RAG Assistant")
app.include_router(admin_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class ChatRequest(BaseModel):
    message: str
    history: list[str] = []

class FeedbackRequest(BaseModel):
    query_id: str
    isHelpful: bool

# --------- Runs at Startup ---------
@app.on_event("startup")
def startup_event():
    if vector_store_is_empty():
        print("Vector DB empty. Building from sources...")
        rebuild_vector_db_internal()

# ---------- Chat Endpoint ----------
@app.post("/ask")
def get_ans(req: ChatRequest):
    message, history = req.message, req.history

    is_unsafe = is_query_unsafe(message)

    rewritten_query = rewrite_query(message, history)
    query_embedding = embed_texts([rewritten_query])[0]
    retrieved_chunks = retrieve_chunks(query_embedding)

    answer = generate_answer(message, retrieved_chunks)

    sources = [e["source"] for e in retrieved_chunks]

    query_id = log_query(
        query=message,
        retrieved_chunks=retrieved_chunks,
        answer=answer,
        is_unsafe=is_unsafe
    )

    return {
        "query_id": query_id,
        "answer": answer,
        "sources": sources,
        "isUnsafe": is_unsafe
    }

# ---------- Feedback Endpoint ----------
@app.post("/feedback")
def store_feedback(req: FeedbackRequest):
    log_feedback(req.query_id, req.isHelpful)
    return {"status": "Feedback recorded"}


# ---------- Home Page ----------
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "out")
app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")