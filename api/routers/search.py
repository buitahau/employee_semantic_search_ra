from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

import query

router = APIRouter()


@router.get("/search")
async def search(q: str = Query(..., description="Search query")):
    try:
        result = query.search(q)
        return JSONResponse(status_code=200, content=result)
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
