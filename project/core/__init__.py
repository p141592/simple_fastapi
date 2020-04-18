import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from core.server import settings
from core.server.application import MIDDLEWARES
from core.server.db import db
from core.server.routes import apps
from core.server.settings import SENTRY_DSN
from core.service import service_route

_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(
            **settings.AppSettings().dict(),
            middleware=MIDDLEWARES
        )

        _app.include_router(service_route)
        _app.include_router(apps)

        if SENTRY_DSN:
            sentry_sdk.init(dsn="https://<key>@<organization>.ingest.sentry.io/<project>")
            _app.add_middleware(SentryAsgiMiddleware)

        db.init_app(_app)
    return _app
