import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import index, search

app = FastAPI(title="Skills Search ETL API", version="0.1.0")
app.include_router(index.router, tags=["index"])
app.include_router(search.router, tags=["search"])

_logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    _logger.error(
        "Unhandled exception on %s %s\n%s",
        request.method,
        request.url.path,
        traceback.format_exc(),
    )
    return JSONResponse(status_code=500, content={"detail": str(exc)})
