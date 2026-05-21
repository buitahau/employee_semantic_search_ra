from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from etl.extract import extract_employee
from etl.transform import transform

router = APIRouter()


@router.get("/extract/{employee_id}")
def get_employee_data(employee_id: int):
    try:
        data = extract_employee(employee_id)
        data = transform(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return asdict(data)
