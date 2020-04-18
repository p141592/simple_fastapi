from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware

from core.server import settings

from apps.access.routes import access

ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
]

MIDDLEWARES = (
    Middleware(PrometheusMiddleware),
    Middleware(CORSMiddleware,
               allow_origins=ORIGINS,
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"]
    ),
)

MOUNTS = (
    ("/static", StaticFiles(directory=settings.STATIC_PATH), dict(name="static")),
    ("/media", StaticFiles(directory=settings.MEDIA_PATH), dict(name="media")),
)

ROUTES = (
    Route('/api/access', access),
)
