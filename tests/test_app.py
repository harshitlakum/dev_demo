from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_echo():
    r = client.post("/echo", json={"msg": "hello"})
    assert r.status_code == 200
    assert r.json() == {"msg": "hello", "length": 5}
