from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    config = Config(str(Path(__file__).resolve().parents[3] / "alembic.ini"))
    command.upgrade(config, "head")
