import os
from docx import Document
from pypdf import PdfReader


def load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                pages.append(text)
        except Exception as e:
            print(f"⚠️ Skipping page {i} due to extraction error: {e}")
    return "\n".join(pages)


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return load_txt(path)
    elif ext == ".docx":
        return load_docx(path)
    elif ext == ".pdf":
        return load_pdf(path)
    else:
        raise ValueError("Unsupported file type")
