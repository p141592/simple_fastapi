from core.routes import routes
from core.server.application import Application
from core.server.db import db

_app = None


def get_app():
    global _app
    if not _app:
        _app = Application()
        db.init_app(_app)
        init_routes(_app)
    return _app


def init_routes(app):
    for _route in routes:
        app.include_router(
            _route[0], **_route[1]
        )


def app():
    return get_app()

