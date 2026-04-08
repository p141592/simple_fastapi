from pathlib import Path

from pydantic import DirectoryPath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PROJECT_DIR.parent


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "debug"
    RELOAD: bool = False
    DEBUG: bool = False
    WORKERS: int = 2
    SENTRY_DSN: str | None = None
    TEMPLATES_DIR: DirectoryPath = PROJECT_DIR / "templates"
    MEDIA_PATH: DirectoryPath = PROJECT_DIR / "media"
    STATIC_PATH: DirectoryPath = PROJECT_DIR / "static"

    DB_PASSWORD: SecretStr = SecretStr("postgres")
    DB_DSN: str = "postgresql://postgres:postgres@localhost:5431/postgres"
    DB_ECHO: bool = False

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")


settings = Settings()
