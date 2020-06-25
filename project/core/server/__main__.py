import uvicorn

from core.settings import RunSettings

if __name__ == "__main__":
    uvicorn.run("asgi:app", **RunSettings().dict())
