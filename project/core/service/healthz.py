from fastapi import APIRouter

route = APIRouter()


@route.get("/healthz")
async def healthz():
    return {"message": "pong"}
