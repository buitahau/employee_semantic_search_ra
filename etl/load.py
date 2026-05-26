import json

from psycopg2.extras import execute_values

from common.db import _vector_connect
from common.types import ChunkRecord

_DELETE_SQL = "DELETE FROM skills_search_index WHERE employee_id = %s"

_INSERT_SQL = """
INSERT INTO skills_search_index
    (employee_id, chunk_index, field_type, chunk_text, embedding, metadata)
VALUES %s
"""


def _to_row(employee_id: int, chunk: ChunkRecord) -> tuple:
    merged_metadata = {
        **chunk.metadata,
        "preprocess_version": chunk.preprocess_version,
        "char_start": chunk.char_start,
        "char_end": chunk.char_end,
        "token_count": chunk.token_count,
    }
    embedding_str = "[" + ",".join(str(x) for x in chunk.embedding) + "]"
    return (
        employee_id,
        chunk.chunk_index,
        chunk.field_type,
        chunk.chunk_text,
        embedding_str,
        json.dumps(merged_metadata),
    )


def load_employee(employee_id: int, chunks: list[ChunkRecord]) -> None:
    missing = [i for i, c in enumerate(chunks) if c.embedding is None]
    if missing:
        raise ValueError(
            f"load_employee: chunks at indices {missing} have embedding=None; "
            "run embed_chunks() before load_employee()"
        )

    with _vector_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(_DELETE_SQL, (employee_id,))
            if chunks:
                rows = [_to_row(employee_id, c) for c in chunks]
                execute_values(cur, _INSERT_SQL, rows, page_size=500)
        conn.commit()
