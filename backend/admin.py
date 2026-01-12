import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File

from backend.job_manager import create_job_entry, get_job_from_db
from db.vector_db import get_collection, reset_collection
from rag.file_processing import process_documents_job

router = APIRouter(prefix="/admin", tags=["Admin"])

SOURCES_DIR = Path("sources")
SOURCES_DIR.mkdir(exist_ok=True)

@router.get("/documents")
def list_documents():
    """
    List all unique ingested documents in the vector DB
    """
    collection = get_collection()
    data = collection.get()

    if not data or not data.get("metadatas"):
        return {"documents": []}

    docs = {}
    for meta in data["metadatas"]:
        doc_id = meta.get("source_doc_id", "unknown")
        docs.setdefault(doc_id, 0)
        docs[doc_id] += 1

    return {
        "total_documents": len(docs),
        "documents": [
            {
                "source_doc_id": k,
                "total_chunks": v
            }
            for k, v in docs.items()
        ]
    }


@router.delete("/documents/{source_doc_id}")
def delete_document(source_doc_id: str):
    """
    Delete all chunks belonging to a specific document
    """
    collection = get_collection()
    data = collection.get()

    if not data or not data.get("ids"):
        raise HTTPException(status_code=404, detail="No documents found")

    ids_to_delete = []
    for idx, meta in zip(data["ids"], data["metadatas"]):
        if meta.get("source_doc_id") == source_doc_id:
            ids_to_delete.append(idx)

    if not ids_to_delete:
        raise HTTPException(status_code=404, detail="Document not found")

    collection.delete(ids=ids_to_delete)

    return {
        "status": "deleted",
        "source_doc_id": source_doc_id,
        "chunks_removed": len(ids_to_delete)
    }


@router.post("/reset")
def admin_reset_db():
    """
    Dangerous operation: clears entire knowledge base
    """
    reset_collection()
    get_collection()
    return {"status": "knowledge base wiped"}



@router.post("/upload")
async def upload_doc(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):  
    """
    Upload PDF / DOCX / TXT and ingest into vector DB
    """
    allowed_ext = {".pdf", ".docx", ".txt"}
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in allowed_ext:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are supported"
        )


    job_id = create_job_entry(filename)

    filepath = SOURCES_DIR / filename
    with open(str(filepath), "wb") as f:
        shutil.copyfileobj(file.file, f)

    background_tasks.add_task(
        process_documents_job,
        job_id,
        str(filepath)
    )

    return {
        "job_id": job_id,
        "status": "processing"
    }


@router.get("/documents/{job_id}/status")
async def get_job_status(job_id: str):
    return get_job_from_db(job_id)

@router.post("/rebuild-vec-db")
def rebuild_vector_db(background_tasks: BackgroundTasks):
    reset_collection()
    get_collection()
    try:
        if not SOURCES_DIR.exists():
            raise HTTPException(status_code=400, detail="No sources directory found")
        
        files = [f for f in SOURCES_DIR.iterdir() if f.is_file()]

        if not files:
            return {"status": "ok", "message": "No documents to process"}
        for file in files:
            job_id=create_job_entry(file.name)
            background_tasks.add_task(
                process_documents_job,
                job_id,
                str(file)
            )
        
        return {"status": "ok", "message": "Rebuild started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
