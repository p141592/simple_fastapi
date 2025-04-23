from fastapi import APIRouter
from pydantic import BaseModel

route = APIRouter()


class HealthResponse(BaseModel):
    message: str


@route.get("/healthz")
async def healthz():
    return HealthResponse(message="pong")
