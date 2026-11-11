from unittest.mock import patch

from fastapi.testclient import TestClient

from agent import app

client = TestClient(app)


def test_api_success():
    with patch("agent.generate", return_value="ok"):
        response = client.post("/ask", json={"prompt": "Hi"})
    assert response.status_code == 200
    assert response.json() == {"response": "ok"}


def test_api_ollama_failure():
    with patch("agent.generate", side_effect=RuntimeError("offline")):
        response = client.post("/ask", json={"prompt": "Hi"})
    assert response.status_code == 503
    assert "offline" in response.json()["detail"]


def test_api_blank_prompt():
    assert client.post("/ask", json={"prompt": ""}).status_code == 422
