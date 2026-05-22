from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from common.config import settings


@contextmanager
def _connect():
    conn = psycopg2.connect(
        host=settings.source_db.host,
        port=settings.source_db.port,
        dbname=settings.source_db.name,
        user=settings.source_db.user,
        password=settings.source_db.password,
    )
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
    finally:
        conn.close()


@contextmanager
def _vector_connect():
    conn = psycopg2.connect(
        host=settings.vector_db.host,
        port=settings.vector_db.port,
        dbname=settings.vector_db.name,
        user=settings.vector_db.user,
        password=settings.vector_db.password,
    )
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
