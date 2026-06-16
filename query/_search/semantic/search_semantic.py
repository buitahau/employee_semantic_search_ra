from query._search.semantic.deduplicate import deduplicate
from query._search.semantic.re_rank import re_rank
from query._search.semantic.retrieve import retrieve
from query.types import QueryAnalysis, SemanticSearchResult


def search_semantic(analysis: QueryAnalysis) -> SemanticSearchResult:
    hits = retrieve(analysis)
    deduped_hits = deduplicate(hits)
    re_ranked_hits = re_rank(deduped_hits)
    return SemanticSearchResult(hits=re_ranked_hits, matched_count=len(re_ranked_hits))
