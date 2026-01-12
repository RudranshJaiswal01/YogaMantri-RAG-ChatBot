import re

def is_query_unsafe(query: str) -> bool:
    triggers = [
        "asthma",
        "fractures",
        "surgery",
        "pregnancy",
        "pregnant",
        "epilepsy",
        "seizures",
        "stroke",
        "heart attack",
        "slip disc"
    ]
    q = query.lower()
    return any(t in q for t in triggers)