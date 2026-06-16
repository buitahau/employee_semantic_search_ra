from etl.extract import extract_employee
from query.types import ExactFilterResult, QueryAnalysis, SearchResult, SemanticSearchResult


def aggregate_results(analysis: QueryAnalysis, exactFilterResult: ExactFilterResult, semanticSearchResult: SemanticSearchResult) -> SearchResult:
    exact_ids = set(exactFilterResult.employee_ids)
    semantic_ids = {hit.employee_id for hit in semanticSearchResult.hits}
    merged_ids = list(exact_ids | semantic_ids)

    results = [extract_employee(eid) for eid in merged_ids]

    return SearchResult(query=analysis.query, total_matches=len(results), results=results)