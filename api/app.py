from fastapi import FastAPI
from api.routers import index, search

app = FastAPI(title="Skills Search ETL API", version="0.1.0")
app.include_router(index.router, tags=["index"])
app.include_router(search.router, tags=["search"])
