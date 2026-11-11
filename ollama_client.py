"""Shared Ollama HTTP client for the Gradio UI and optional FastAPI app."""

import os

import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "120"))


def generate(prompt: str) -> str:
    """Generate a response or raise a human-readable RuntimeError."""
    if not prompt or not prompt.strip():
        raise ValueError("Please enter a prompt.")

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt.strip(), "stream": False},
            timeout=OLLAMA_TIMEOUT,
        )
        response.raise_for_status()
        result = response.json()
    except requests.Timeout as exc:
        raise RuntimeError(
            "Ollama timed out. Check model availability and try again."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_HOST}. Is the service running?"
        ) from exc
    except ValueError as exc:
        raise RuntimeError("Ollama returned an invalid JSON response.") from exc

    if "error" in result:
        raise RuntimeError(f"Ollama error: {result['error']}")
    text = result.get("response", "")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("Ollama returned an empty response.")
    return text.strip()
