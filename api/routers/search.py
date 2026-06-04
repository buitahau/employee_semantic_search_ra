import json
from datetime import date, datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

import query

router = APIRouter()


def _default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
async def search(body: SearchRequest):
    try:
        result = query.search(body.query)
        return Response(
            content=json.dumps(result, default=_default),
            status_code=200,
            media_type="application/json",
        )
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
