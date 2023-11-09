import pytest

from fastapi.testclient import TestClient

from api.__main__ import setup_server


@pytest.fixture(scope="class")
def client():
    client = TestClient(setup_server())
    yield client



@pytest.mark.usefixtures(
    "client"
)
class TestApp:
    def test_root(self, client):
        assert client.get("/").json() == {
            "response":"this is the root of the fastAPI API"
        }

    def test_items(self, client):
        resp = client.delete("/items")

        assert resp.status_code == 204

        data = dict(
            name="this",
            description="that"
        )

        resp = client.post("/items", params=data)

        assert resp.status_code == 201

        resp = client.get("/items")

        assert resp.status_code == 200

        item = resp.json()["items"].pop()
        item_id = item.split("/").pop()
        resp = client.get(f"/item/{item_id}")
        _, v = resp.json()["item"].popitem()
        for key in data.keys():
            assert data[key] == v[key]


        resp = client.delete("/items")

        assert resp.status_code == 204
