import pytest
from alembic.config import main
from starlette.config import environ
from starlette.testclient import TestClient

environ["TESTING"] = "1"


@pytest.fixture
def client():
    from core.application import get_app

    main(["--raiseerr", "upgrade", "head"])

    with TestClient(get_app()) as client:
        yield client

    main(["--raiseerr", "downgrade", "base"])
