"""
Write a minimal MongoDB utility module using PyMongo for a RAG-based wellness application.

Requirements:
- Use PyMongo (no ODM or ORM).
- MongoDB is used ONLY for logging and audit purposes, not for retrieval.
- Provide sensible default configuration so the file works without a .env file.

Configuration:
- Read MongoDB URI from environment variable MONGO_URI, default to "mongodb://localhost:27017".
- Read database name from environment variable DB_NAME, default to "wellness_rag".

Collections:
1. query_logs
   Stores each user interaction with the RAG system.

2. feedback_logs
   Stores optional user feedback (thumbs up / thumbs down).

Functions to implement:

1. log_query(query: str, retrieved_chunks: list, answer: str, is_unsafe: bool) -> str
   - Inserts a document into query_logs with the following fields:
     - query (string): the raw user query
     - retrievedChunks (list): list of retrieved chunk identifiers and sources
     - answer (string): final AI-generated answer
     - isUnsafe (boolean): whether safety filter was triggered
     - timestamp (UTC datetime)
   - Return the inserted document ID as a string.

2. log_feedback(query_id: str, helpful: bool) -> None
   - Inserts a document into feedback_logs with:
     - queryId (string)
     - helpful (boolean)
     - timestamp (UTC datetime)

Other constraints:
- Do not implement read/query APIs.
- Do not add indexes or schema validation.
- Keep the file small, clean, and readable.
- Handle MongoDB connection at module level so it is reused across imports.
"""
import os
from datetime import datetime
from pymongo import MongoClient

# Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "yogamantri"

# Initialize MongoDB connection
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def log_query(query: str, retrieved_chunks: list, answer: str, is_unsafe: bool) -> str:
    doc = {
        "query": query,
        "retrievedChunks": retrieved_chunks,
        "answer": answer,
        "isUnsafe": is_unsafe,
        "timestamp": datetime.utcnow()
    }
    result = db.query_logs.insert_one(doc)
    return str(result.inserted_id)

def log_feedback(query_id: str, helpful: bool) -> None:
    doc = {
        "helpful": helpful,
        "timestamp": datetime.utcnow()
    }
    db.feedback_logs.update_one(
        {"queryId": query_id},
        {"$set": doc},
        upsert=True
    )

