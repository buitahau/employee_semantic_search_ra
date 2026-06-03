from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from query.types import QueryRequest

router = APIRouter()


@router.get("/search")
async def search(request: Annotated[QueryRequest, Body()]):
    return JSONResponse(status_code=200, content={"message": "ok"})
