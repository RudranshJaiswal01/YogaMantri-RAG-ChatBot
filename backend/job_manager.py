from datetime import datetime
from typing import Dict

JOBS: Dict[str, dict] = {}

def create_job_entry(filename):
    job_id = f"job_{len(JOBS)+1}"

    JOBS[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "file": filename,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": None,
        "error": None
    }

    return job_id


def update_job_status(job_id: str, status: str, error: str = None):
    if job_id not in JOBS:
        return

    JOBS[job_id]["status"] = status
    JOBS[job_id]["updated_at"] = datetime.utcnow().isoformat()
    JOBS[job_id]["error"] = error


def get_job_from_db(job_id: str):
    return JOBS.get(job_id)
