from pathlib import Path

import psycopg2
from fastapi import APIRouter, HTTPException

from common.config import settings
from etl import run_employee_pipeline
from etl.extract import get_all_employee_ids

router = APIRouter()

_SEED_SQL = Path(__file__).parent.parent.parent / "migrations" / "local" / "seed_data.sql"


@router.post("/index/{employee_id}", status_code=200)
def index_employee(employee_id: int):
    try:
        chunk_count = run_employee_pipeline(employee_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"employee_id": employee_id, "chunks_indexed": chunk_count}


@router.post("/re_index_all", status_code=200)
def re_index_all():
    try:
        employee_ids = get_all_employee_ids()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = []
    for employee_id in employee_ids:
        try:
            chunk_count = run_employee_pipeline(employee_id)
            results.append({"employee_id": employee_id, "chunks_indexed": chunk_count, "status": "ok"})
        except Exception as e:
            results.append({"employee_id": employee_id, "chunks_indexed": 0, "status": "error", "detail": str(e)})

    return {"total": len(employee_ids), "results": results}


@router.post("/load_seed_data", status_code=200)
def load_seed_data():
    if settings.source_db.host not in ("localhost", "127.0.0.1"):
        raise HTTPException(status_code=403, detail="load_seed_data is only allowed when SOURCE_DB_HOST is localhost")

    sql = _SEED_SQL.read_text()

    try:
        src_conn = psycopg2.connect(
            host=settings.source_db.host,
            port=settings.source_db.port,
            dbname=settings.source_db.name,
            user=settings.source_db.user,
            password=settings.source_db.password,
        )
        src_conn.autocommit = True
        with src_conn.cursor() as cur:
            cur.execute(sql)
        src_conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"seed source DB failed: {e}")

    try:
        vec_conn = psycopg2.connect(
            host=settings.vector_db.host,
            port=settings.vector_db.port,
            dbname=settings.vector_db.name,
            user=settings.vector_db.user,
            password=settings.vector_db.password,
        )
        with vec_conn.cursor() as cur:
            cur.execute("DELETE FROM skills_search_index")
        vec_conn.commit()
        vec_conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"clear embedding DB failed: {e}")

    return {"status": "ok"}
