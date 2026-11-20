from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_review_rejects_empty_code():
    response = client.post("/review", json={"code": ""})
    assert response.status_code == 422

def test_review_endpoint(monkeypatch):
    def fake_invoke(state):
        return {"review": "No major issues found.", "refactored_code": "print('hello')"}

    monkeypatch.setattr("app.main.agent_graph.invoke", fake_invoke)
    response = client.post("/review", json={"code": "print('hello')"})
    assert response.status_code == 200
    assert response.json()["review"] == "No major issues found."
    assert response.json()["refactored_code"] == "print('hello')"
