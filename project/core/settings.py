import os
from pathlib import Path

from pydantic import BaseSettings

e = os.environ.get

version = e("APP_VERSION", "0.0.1")


class AppSettings(BaseSettings):
    title: str = "Simple FastAPI"
    version: str = version
    description: str = ""
    docs_url: str = "/swagger"
    db_connect: str = "mongodb://localhost:27017"
    db_name: str = "test"
    static_path: str = e("STATIC_PATH", str(Path(".").parent.parent / "static"))
    media_path: str = e("MEDIA_PATH", str(Path(".").parent.parent / "media"))
    secret_key: str = e("SECRET_KEY", "fake")


class RunSettings(BaseSettings):
    reload: bool = bool(e("DEBUG"))
    debug: bool = bool(e("DEBUG"))
    host: str = e("HOST", "0.0.0.0")
    port: int = int(e("PORT", 8000))
    log_level: str = "debug"
