from pathlib import Path

from rag.file_loader import extract_text_from_file
from rag.chunking import chunk_text
from rag.store_chunks import store_chunks
from backend.job_manager import update_job_status

def process_documents(filepath: str):
    try:
        print("File Processing...")
        print("Step 1: Extracting text from file.")
        text = extract_text_from_file(filepath)

        if not text.strip():
            raise(filepath," is empty")

        print("Step 2: Chunking text.")
        chunks = chunk_text(text)

        for c in chunks:
            c["metadata"]["source_doc_id"] = Path(filepath).name

        print("Step 3: Storing chunks in vector database.")
        store_chunks(chunks)
        return "Success", "no error"

    except Exception as e:
        return "Error Occurred", "Error: " + str(e)
        
    finally:
        print("File Processing Completed.")

def process_documents_job(job_id: str, filepath: str):
    print(f"Job {job_id} started for processing documents.")
    status, error = process_documents(filepath)
    print(f"Job {job_id} finished processing documents.")
    update_job_status(job_id, status=status, error=error)