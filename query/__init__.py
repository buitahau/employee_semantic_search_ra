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
    return {"query": query, "total": len(re_ranked_hits), "data": [asdict(h) for h in re_ranked_hits]}

    # return {
    #     "query": asdict(analysis),
    #     "response": {"total": len(re_ranked_hits), "data": [asdict(h) for h in re_ranked_hits]},
    #     "re_ranked_hits": {"total": len(re_ranked_hits), "data": [asdict(h) for h in re_ranked_hits]},
    #     "deduped_hits": {"total": len(deduped_hits), "data": [asdict(h) for h in deduped_hits]},
    #     "hits": {"total": len(hits), "data": [asdict(h) for h in hits]},
    #     }