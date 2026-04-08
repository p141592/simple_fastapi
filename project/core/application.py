import sentry_sdk
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from apps.routes import router
from core.db import run_migrations
from core.settings import settings
from core.service import service_route

app_instance = None

ORIGINS = ["*"]
MOUNTS = (
    ("/static", StaticFiles(directory=settings.STATIC_PATH), {"name": "static"}),
    ("/media", StaticFiles(directory=settings.MEDIA_PATH), {"name": "media"}),
)


class CustomApp(FastAPI):
    templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    del app
    run_migrations()
    yield


def get_app() -> FastAPI:
    global app_instance
    if app_instance is None:
        app_instance = CustomApp(
            title="FastAPI backend template",
            version="1.0.0",
            lifespan=lifespan,
            middleware=(
                Middleware(
                    CORSMiddleware,
                    allow_origins=ORIGINS,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                ),
            ),
        )
        app_instance.include_router(service_route)
        app_instance.include_router(router)

        for mount in MOUNTS:
            app_instance.mount(*mount)

        if settings.SENTRY_DSN:
            sentry_sdk.init(dsn=settings.SENTRY_DSN)
            app_instance.add_middleware(SentryAsgiMiddleware)

    return app_instance


if __name__ == "__main__":
    uvicorn.run(
        "project.asgi:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
