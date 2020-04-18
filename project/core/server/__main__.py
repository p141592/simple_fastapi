import uvicorn

from core.server import settings

if __name__ == '__main__':
    uvicorn.run("project.asgi:app", **settings.RunSettings().dict())
