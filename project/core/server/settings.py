import os
from pathlib import Path

from pydantic import BaseSettings
from sqlalchemy.engine.url import make_url, URL
from starlette.config import Config
from starlette.datastructures import Secret

e = os.environ.get


class AppSettings(BaseSettings):
    title: str = "Simple FastAPI"
    version: str = "0.0.1"
    description: str = ""
    docs_url: str = "/swagger"


class RunSettings(BaseSettings):
    reload: bool = bool(e("DEBUG"))
    debug: bool = bool(e("DEBUG"))
    host: str = e("HOST", "0.0.0.0")
    port: int = int(e("PORT", 8000))
    log_level: str = "debug"


config = Config(".env")

TESTING = config("TESTING", cast=bool, default=False)
SECRET = config("SECRET", default="fake")
MEDIA_PATH = config("MEDIA_PATH", default=str(Path(__file__).parent.absolute() / "media"))
STATIC_PATH = config("STATIC_PATH", default=str(Path(__file__).parent.absolute() / "static"))
DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_USER = config("DB_USER", default="postgres")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
DB_NAME = config("DB_NAME", default=None)
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    ),
)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=1)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)

SENTRY_DSN = config("SENTRY_DSN", default=None)
