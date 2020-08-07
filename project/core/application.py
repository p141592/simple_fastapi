import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware

from apps.routes import router
from core.db import db
from core.settings import settings
from core.service import service_route

_app = None

ORIGINS = [
    "*",
]

MOUNTS = (
    ("/static", StaticFiles(directory=settings.STATIC_PATH), dict(name="static")),
    ("/media", StaticFiles(directory=settings.MEDIA_PATH), dict(name="media")),
)


class CustomApp(FastAPI):
    templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def get_app():
    global _app
    if not _app:
        _app = CustomApp(
            title="FastAPI backend template",
            version="0.0.4",
            description="",
            exception_handlers=None,
            middleware=(
                Middleware(PrometheusMiddleware),
                Middleware(
                    CORSMiddleware,
                    allow_origins=ORIGINS,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                ),
            ),
        )

        _app.include_router(service_route)
        _app.include_router(router)

        for _mount in MOUNTS:
            _app.mount(*_mount)

        if settings.SENTRY_DSN:
            sentry_sdk.init(dsn=settings.SENTRY_DSN)
            _app.add_middleware(SentryAsgiMiddleware)
        db.init_app(_app)

    return _app


if __name__ == "__main__":
    uvicorn.run(
        "asgi:app",
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        http="h11",
        loop="asyncio",
    )
