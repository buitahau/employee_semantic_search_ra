from fastapi import APIRouter

router = APIRouter()


@router.get("/search")
async def search():
    raise NotImplementedError
