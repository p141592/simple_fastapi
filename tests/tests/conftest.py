import pytest
from fastapi.testclient import TestClient

from project.core.server import app


@pytest.fixture
def client():
    return TestClient(app)
