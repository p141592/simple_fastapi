import uvicorn

from core import settings

if __name__ == "__main__":
    uvicorn.run("asgi:app", **settings.RunSettings().dict())