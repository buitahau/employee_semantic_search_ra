from query.impl.analyze_query.metadata import build_filter
from query.types import QueryAnalysis


def analyze_query(normalized: str) -> QueryAnalysis:
    return QueryAnalysis(
        intent="find_employees",
        query=normalized,
        heuristic="rank employees by score descending",
        filter=build_filter(normalized),
    )
