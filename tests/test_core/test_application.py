import pytest


class TestApplication:
    def test_ping(self, client):
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}

    @pytest.mark.parametrize("source", ["/static/test.jpg", "/media/test.jpg"])
    def test_static_path(self, source, client):
        response = client.get(source)
        assert response.status_code == 200

    def test_metrics(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_user_crud(self, client):
        created = client.post("/user/v1/users", json={"name": "Alice"})
        assert created.status_code == 201
        created_payload = created.json()
        assert created_payload["name"] == "Alice"
        assert isinstance(created_payload["id"], int)

        user_id = created_payload["id"]

        fetched = client.get(f"/user/v1/users/{user_id}")
        assert fetched.status_code == 200
        assert fetched.json() == created_payload

        deleted = client.delete(f"/user/v1/users/{user_id}")
        assert deleted.status_code == 200
        assert deleted.json() == {"id": user_id}

        missing = client.get(f"/user/v1/users/{user_id}")
        assert missing.status_code == 404
        assert missing.json() == {"detail": "User not found"}
