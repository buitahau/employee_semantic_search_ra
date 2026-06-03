from query.normalize import normalize_query


def search(query: str) -> dict:
    normalized = normalize_query(query)
    return {"query": normalized}
