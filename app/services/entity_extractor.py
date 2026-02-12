import re
from collections import Counter
from typing import List

from app.schemas.article_schema import EntitySummary


def _candidate_proper_nouns(text: str) -> List[str]:
    """Very lightweight heuristic to pull capitalised tokens as entities."""
    tokens = re.findall(r"\b[A-Z][a-zA-Z\-]{2,}\b", text)
    return tokens


def extract_entities(text: str) -> EntitySummary:
    """Extract rough entities (people, organizations, locations) from text.

    For production you might plug in spaCy or a hosted NER model.
    Here we use simple heuristics and frequency counts for determinism.
    """
    tokens = _candidate_proper_nouns(text)
    counts = Counter(tokens)

    # Pick top N as generic entities, then loosely categorise by suffixes.
    common = [tok for tok, _ in counts.most_common(50)]

    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []

    for name in common:
        lower = name.lower()
        if lower.endswith(("inc", "corp", "university", "committee", "council")):
            organizations.append(name)
        elif lower.endswith(("city", "state", "province", "kingdom", "republic")):
            locations.append(name)
        else:
            people.append(name)

    # De-duplicate while preserving order
    def dedupe(seq: List[str]) -> List[str]:
        seen = set()
        result: List[str] = []
        for item in seq:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    return EntitySummary(
        people=dedupe(people[:20]),
        organizations=dedupe(organizations[:20]),
        locations=dedupe(locations[:20]),
    )

