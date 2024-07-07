from fastapi import FastAPI
from pydantic import BaseModel

from utils import bulk_rolls, search_bulk_worksheet

app = FastAPI()


class BulkRequest(BaseModel):
    roll_f: str
    roll_l: str
    sem: int
    sub: str
    week: int


@app.get("/")
async def root():
    return {"status": "Working"}


@app.post("/bulk")
async def bulk(request: BulkRequest):
    return search_bulk_worksheet(bulk_rolls(request.roll_f, request.roll_l), request.sem, request.sub, request.week)
