from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, SecretStr

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "debug"
    RELOAD: bool = True
    DEBUG: bool = False
    WORKERS: int = 2
    SENTRY_DSN: str = None
    TEMPLATES_DIR: DirectoryPath = BASE_DIR / "templates"
    MEDIA_PATH: DirectoryPath = BASE_DIR / "media"
    STATIC_PATH: DirectoryPath = BASE_DIR / "static"

    DB_PASSWORD: SecretStr = "postgres"
    DB_DSN: str = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/postgres"
    DB_POOL_MIN_SIZE: int = 1
    DB_POOL_MAX_SIZE: int = 16
    DB_ECHO: bool = True
    DB_SSL: str = None
    DB_USE_CONNECTION_FOR_REQUEST: bool = True
    DB_RETRY_LIMIT: int = 1
    DB_RETRY_INTERVAL: int = 1

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
