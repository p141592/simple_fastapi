from fastapi import FastAPI

from core.server import settings
from core.server.application import ROUTES, MIDDLEWARES
from core.server.db import db
from core.service import service_route
from core.utils.routes import init_routes

_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(
            **settings.AppSettings().dict(),
            routes=ROUTES,
            middleware=MIDDLEWARES
        )
        _app.include_router(service_route, tags=['system'])

        db.init_app(_app)
    return _app
