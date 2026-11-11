from unittest.mock import Mock

import pytest
import requests

import ollama_client


def test_generate_success(monkeypatch):
    response = Mock()
    response.json.return_value = {"response": "  Hello!  "}
    response.raise_for_status.return_value = None
    post = Mock(return_value=response)
    monkeypatch.setattr(ollama_client.requests, "post", post)
    monkeypatch.setattr(ollama_client, "OLLAMA_HOST", "http://ollama:11434")
    monkeypatch.setattr(ollama_client, "OLLAMA_TIMEOUT", 9.0)
    assert ollama_client.generate(" Hi ") == "Hello!"
    post.assert_called_once_with(
        "http://ollama:11434/api/generate",
        json={"model": ollama_client.OLLAMA_MODEL, "prompt": "Hi", "stream": False},
        timeout=9.0,
    )


def test_blank_prompt_never_calls_ollama(monkeypatch):
    post = Mock()
    monkeypatch.setattr(ollama_client.requests, "post", post)
    with pytest.raises(ValueError, match="enter a prompt"):
        ollama_client.generate("  ")
    post.assert_not_called()


@pytest.mark.parametrize("error", [requests.Timeout(), requests.ConnectionError()])
def test_network_errors(monkeypatch, error):
    monkeypatch.setattr(
        ollama_client.requests, "post", Mock(side_effect=error)
    )
    with pytest.raises(RuntimeError):
        ollama_client.generate("Hi")


def test_http_failure(monkeypatch):
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    monkeypatch.setattr(ollama_client.requests, "post", Mock(return_value=response))
    with pytest.raises(RuntimeError, match="Could not reach Ollama"):
        ollama_client.generate("Hi")


def test_invalid_json(monkeypatch):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.side_effect = ValueError("bad JSON")
    monkeypatch.setattr(ollama_client.requests, "post", Mock(return_value=response))
    with pytest.raises(RuntimeError, match="invalid JSON"):
        ollama_client.generate("Hi")


@pytest.mark.parametrize("data", [{"response": ""}, {"error": "model unavailable"}])
def test_ollama_error_payloads(monkeypatch, data):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = data
    monkeypatch.setattr(ollama_client.requests, "post", Mock(return_value=response))
    with pytest.raises(RuntimeError):
        ollama_client.generate("Hi")
