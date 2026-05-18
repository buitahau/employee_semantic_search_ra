from fastapi import APIRouter

router = APIRouter()


@router.post("/index", status_code=202)
async def index():
    raise NotImplementedError
