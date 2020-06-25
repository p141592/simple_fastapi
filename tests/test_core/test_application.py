import pytest


class TestApplication:
    def test_ping(self, client):
        """Проверка, что приложение может отвечать на запросы"""
        resp = client.get("/healthz")
        assert resp.status_code == 200
        assert resp.json() == {"message": "pong"}

    @pytest.mark.parametrize(
        "source", ["/static/test.jpg", "/media/test.jpg",],
    )
    def test_static_path(self, source, client):
        """Проверка существования и доступности папки static, media и вложенных папок"""
        resp = client.get(source)
        assert resp.status_code == 200
