import os
from pathlib import Path

from pydantic import BaseSettings, SecretStr, DirectoryPath

BASE_DIR = Path(__file__).parent.parent

e = os.environ.get


def get_env_path():
    _path = (
        (BASE_DIR / ".env.local"),
        (BASE_DIR / ".env"),
        (BASE_DIR.parent / ".env.local"),
        (BASE_DIR.parent / ".env"),
    )
    for _p in _path:
        if _p.exists():
            return _p.resolve()


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

    class Config:
        env_file = get_env_path()


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "debug"
    RELOAD: bool = True
    DEBUG: bool = False
    SENTRY_DSN: str = None
    DB_PASSWORD: SecretStr = "postgres"
    DB_DSN: str = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/postgres"
    DB_POOL_MIN_SIZE: int = 1
    DB_POOL_MAX_SIZE: int = 16
    DB_ECHO: bool = True
    DB_SSL: str = None
    DB_USE_CONNECTION_FOR_REQUEST: bool = True
    DB_RETRY_LIMIT: int = 1
    DB_RETRY_INTERVAL: int = 1
    TEMPLATES_DIR: DirectoryPath = BASE_DIR / "templates"
    MEDIA_PATH: DirectoryPath = BASE_DIR / "media"
    STATIC_PATH: DirectoryPath = BASE_DIR / "static"

    class Config:
        env_file = get_env_path()


settings = Settings()
