from query.analyze_query import analyze_query
from query.normalize import normalize_query


def search(query: str) -> dict:
    normalized = normalize_query(query)
    analysis = analyze_query(normalized)
    return {"query": analysis}
