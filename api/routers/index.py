from fastapi import APIRouter, HTTPException

from etl import run_employee_pipeline
from etl.extract import get_all_employee_ids

router = APIRouter()


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
