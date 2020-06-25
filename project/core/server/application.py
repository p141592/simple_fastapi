from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware

from core import settings

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

#
# async def not_found(request, exc):
#     return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)
#
#
# async def server_error(request, exc):
#     return HTMLResponse(content=HTML_500_PAGE, status_code=exc.status_code)
#
# exception_handlers = {
#     404: not_found,
#     500: server_error
# }
