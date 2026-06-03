from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import query

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
async def search(body: SearchRequest):
    try:
        result = query.search(body.query)
        return JSONResponse(status_code=200, content=result)
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
