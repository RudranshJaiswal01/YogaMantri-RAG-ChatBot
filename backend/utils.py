import re

SAFETY_PATTERNS = [
    # Pregnancy
    r"\bpregnan(t|cy)\b",
    r"\btrimester\b",
    r"\bpost\s?partum\b",
    r"\bafter delivery\b",

    # Cardiovascular
    r"\bheart\b",
    r"\bheart attack\b",
    r"\bcardiac\b",
    r"\bblood pressure\b",
    r"\bhigh bp\b",
    r"\bhypertension\b",
    r"\bhypotension\b",
    r"\bstroke\b",

    # Neurological
    r"\bepilepsy\b",
    r"\bseizures?\b",
    r"\bfainting\b",
    r"\bvertigo\b",
    r"\bdizziness\b",

    # Musculoskeletal / Spine
    r"\bslip disc\b",
    r"\bherniated disc\b",
    r"\bdisc bulge\b",
    r"\bspinal injury\b",
    r"\bneck pain\b",
    r"\bback injury\b",
    r"\bspondylitis\b",
    r"\bsciatica\b",

    # Eye / ENT
    r"\bglaucoma\b",
    r"\bretinal\b",
    r"\beye pressure\b",
    r"\bear problem\b",

    # Surgery / Recovery
    r"\bsurgery\b",
    r"\boperation\b",
    r"\bpost surgery\b",
    r"\brecent surgery\b",
    r"\bstitches\b",

    # Other
    r"\basthma\b",
    r"\bbreathing problem\b",
    r"\bhernia\b",
    r"\bosteoporosis\b",
    r"\barthritis\b",
    r"\bchronic pain\b",
]

def is_query_unsafe(query: str) -> bool:
    q = query.lower()
    return any(re.search(pattern, q) for pattern in SAFETY_PATTERNS)
