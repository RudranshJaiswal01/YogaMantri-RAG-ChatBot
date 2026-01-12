from pathlib import Path
from backend.job_manager import create_job_entry
from db.vector_db import get_collection, reset_collection
from rag.file_processing import process_documents_job

SOURCES_DIR = Path("sources")
SOURCES_DIR.mkdir(exist_ok=True)

def rebuild_vector_db_internal():
    reset_collection()
    get_collection()

    if not SOURCES_DIR.exists():
        return

    files = [f for f in SOURCES_DIR.iterdir() if f.is_file()]
    if not files:
        return

    for file in files:
        job_id = create_job_entry(file.name)
        process_documents_job(job_id, str(file))
