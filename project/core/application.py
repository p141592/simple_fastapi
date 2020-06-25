import sentry_sdk
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from core import settings
from core.server.application import MIDDLEWARES
from core.routes import apps
from core.settings import settings, AppSettings
from core.service import service_route

_app = None


class CustomApp(FastAPI):
    templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def get_app():
    global _app
    if not _app:
        _app = CustomApp(**AppSettings().dict(), middleware=MIDDLEWARES)

        _app.include_router(service_route)
        _app.include_router(apps)

        if settings.SENTRY_DSN:
            sentry_sdk.init(dsn=settings.SENTRY_DSN)
            _app.add_middleware(SentryAsgiMiddleware)

    return _app