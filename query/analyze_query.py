from query.impl.analyze_query.intent import detect_intent
from query.impl.analyze_query.metadata import build_filter
from query.types import QueryAnalysis


def analyze_query(normalized: str) -> QueryAnalysis:
    return QueryAnalysis(
        intent=detect_intent(normalized),
        query=normalized,
        heuristic="",
        filter=build_filter(normalized),
    )
