from query.analyze_query import analyze_query
from query.normalize import normalize_query
from query.retrieve import retrieve


def search(query: str) -> dict:
    normalized = normalize_query(query)
    analysis = analyze_query(normalized)
    hits = retrieve(analysis)
    return {"query": analysis, "hits": hits}
