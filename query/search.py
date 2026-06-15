from re import search

from query._aggregate.aggregate import aggregate_results
from query.analyze_query import analyze_query
from query._search.exact_filter.search_exact import search_exact
from query._search.semantic.search_semantic import search_semantic
from query.normalize import normalize_query

from query.types import SearchResult


def query(query: str) -> SearchResult:
    normalized = normalize_query(query)
    analysis = analyze_query(normalized)

    exactFilterResult = search_exact(analysis)
    semanticSearchResult = search_semantic(analysis)
    return aggregate_results(analysis, exactFilterResult, semanticSearchResult)