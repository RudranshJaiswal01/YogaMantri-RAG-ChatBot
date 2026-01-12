from backend.get_groq_client import get_groq_client

MAX_HISTORY = 5

SYSTEM_PROMPT = """
You rewrite questions to be standalone and clear.
Do NOT answer the question.
Do NOT add new information.
Do NOT change the user's intent.
Only resolve references using the conversation history.
"""


def rewrite_query(query: str, history: list[str]) -> str:
    client = get_groq_client()

    if not history:
        return query

    history = history[-MAX_HISTORY:]
    formatted_history = "\n".join(f"- {h}" for h in history)

    prompt = f"""
Conversation history:
{formatted_history}

Current question:
{query}

Rewrite the question so it can be understood on its own.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        top_p=1,
        max_tokens=256
    )

    rewritten = response.choices[0].message.content.strip()
    return rewritten.strip('"').strip("'")
