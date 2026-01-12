from backend.get_groq_client import get_groq_client

SYSTEM_PROMPT = """
You are an AI assistant answering questions strictly using the provided document excerpts.

Rules:
- Use ONLY the provided document excerpts.
- Do NOT mention citations or sources in the answer text.
- Do NOT reference documents explicitly.
- If the answer is not explicitly present, reply with exactly:
"This information is not present in the document."
"""

def generate_answer(question: str, evidence: list[dict]) -> str:
    client = get_groq_client()

    if not evidence:
        return "This information is not present in the document."

    excerpts = "\n\n".join(
        f"[SOURCE]\n{e['text']}\n[CITATION]\n{e['source']}"
        for e in evidence
    )

    user_prompt = f"""
Question:
{question}

Document excerpts:
{excerpts}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
    )

    return response.choices[0].message.content.strip()
