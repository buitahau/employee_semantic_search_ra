from query.types import ChunkHit


def deduplicate(hits: list[ChunkHit]) -> list[ChunkHit]:
    seen: set[int] = set()
    result: list[ChunkHit] = []
    for hit in hits:
        if hit.employee_id not in seen:
            seen.add(hit.employee_id)
            result.append(hit)
    return result
