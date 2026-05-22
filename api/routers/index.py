from fastapi import APIRouter, HTTPException

from etl import run_employee_pipeline

router = APIRouter()


@router.post("/index/{employee_id}", status_code=200)
def index_employee(employee_id: int):
    try:
        chunk_count = run_employee_pipeline(employee_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"employee_id": employee_id, "chunks_indexed": chunk_count}
