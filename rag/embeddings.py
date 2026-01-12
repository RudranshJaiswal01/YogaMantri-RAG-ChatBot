import os
import requests
from typing import List

HF_API_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-base-en-v1.5"


def embed_texts(texts: List[str]) -> List[List[float]]:
    HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
    if not HF_API_TOKEN:
        raise RuntimeError("HF_API_TOKEN not set")

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={
            "inputs": texts,
            "options": {"wait_for_model": True}
        },
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(f"HuggingFace API error: {response.text}")

    embeddings = response.json()

    processed = []

    for emb in embeddings:
        # Case 1: already pooled → [dims]
        if isinstance(emb[0], float):
            processed.append(emb)
        # Case 2: token-level → [tokens, dims]
        else:
            pooled = [sum(col) / len(col) for col in zip(*emb)]
            processed.append(pooled)

    return processed
