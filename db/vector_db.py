import chromadb
from chromadb.config import Settings
from pathlib import Path

VEC_DB_DIR = Path(__file__).resolve().parents[1] / "db" / "vector" / "chroma"
VEC_DB_DIR.mkdir(parents=True, exist_ok=True)
PERSIST_DIR = str(VEC_DB_DIR)
COLLECTION_NAME = "chunks"

_client = chromadb.Client(
    Settings(
        persist_directory=PERSIST_DIR,
        anonymized_telemetry=False
    )
)

def get_collection():
    return _client.get_or_create_collection(COLLECTION_NAME)

def reset_collection():
    try:
        _client.delete_collection(COLLECTION_NAME)
    except Exception as e:
        print("Error Occured During resetting the vectordb, error: ", str(e))

def vector_store_is_empty():
    collection = get_collection()
    return collection.count() == 0
