from dataclasses import asdict

from query.analyze_query import analyze_query
from query.impl.aggregate.deduplicate import deduplicate
from query.impl.aggregate.re_rank import re_rank
from query.normalize import normalize_query
from query.retrieve import retrieve


def search(query: str) -> dict:
    normalized = normalize_query(query)
    analysis = analyze_query(normalized)
    hits = retrieve(analysis)
    deduped_hits = deduplicate(hits)
    re_ranked_hits = re_rank(deduped_hits)
    return {
        "query": asdict(analysis),
        "re_ranked_hits": [asdict(h) for h in re_ranked_hits],
        "deduped_hits": [asdict(h) for h in deduped_hits],
        # "hits": [asdict(h) for h in hits]
        } 