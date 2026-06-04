from query.types import ChunkHit

_THRESHOLD = 0.5


def re_rank(hits: list[ChunkHit]) -> list[ChunkHit]:
    filtered = [h for h in hits if h.score >= _THRESHOLD]
    return sorted(filtered, key=lambda h: h.score, reverse=True)
