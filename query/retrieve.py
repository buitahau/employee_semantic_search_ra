import json
import logging

import psycopg2.extras

from common.db import _vector_connect
from common.embedding import embed
from query.types import ChunkHit, QueryAnalysis

_logger = logging.getLogger(__name__)

_SQL_BASE = """
    SELECT
        employee_id,
        field_type,
        chunk_text,
        metadata,
        1 - (embedding <=> %s::vector) AS similarity
    FROM skills_search_index
    ORDER BY embedding <=> %s::vector
    LIMIT 100
"""


def retrieve(analysis: QueryAnalysis) -> list[ChunkHit]:
    vector = embed(analysis.query)
    vector_str = json.dumps(vector)
    params = (vector_str, vector_str)
    sql = _SQL_BASE

    with _vector_connect() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    return [
        ChunkHit(
            employee_id=row["employee_id"],
            field_type=row["field_type"],
            chunk_text=row["chunk_text"],
            metadata=dict(row["metadata"]),
            score=float(row["similarity"]),
        )
        for row in rows
    ]
