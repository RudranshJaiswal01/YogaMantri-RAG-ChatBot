import uuid

from rag.embeddings import embed_texts
from db.vector_db import get_collection


def store_chunks(chunks: list):
    collection = get_collection()

    texts = []
    metadatas = []
    ids = []
    print(f"Storing {len(chunks)} chunks...")
    for chunk in chunks:
        text = chunk["text"]
        meta = chunk["metadata"].copy()

        section = meta.get("section", "General")
        page_start = meta.get("page_start")
        page_end = meta.get("page_end")
        source_doc_id = meta.get("source_doc_id", "unknown_document")

        if page_start is not None and page_end is not None:
            source = f"{source_doc_id} → {section} (pp. {page_start}–{page_end})"
        else:
            source = f"{source_doc_id} → {section}"

        print("storing chunk with source:", source)
        meta["source"] = source

        texts.append(text)
        metadatas.append(meta)
        ids.append(str(uuid.uuid4()))

    embeddings = embed_texts(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
