from db.vector_db import get_collection

TOP_K = 3
MAX_DISTANCE_THRESHOLD = 1.5


def retrieve_chunks(query_embedding: list[float]) -> list[dict]:
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"]
    )

    if not results["documents"] or not results["documents"][0]:
        return []

    chunks = []

    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if distance > MAX_DISTANCE_THRESHOLD:
            continue

        chunks.append({
            "text": text,
            "source": meta["source"],
            "distance": distance
        })

    # Explicitly sort by relevance
    chunks.sort(key=lambda x: x["distance"])

    return chunks