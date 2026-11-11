# Local AI Chatbot — Gradio + Ollama + Mistral

A minimal self-hosted chatbot using a Gradio UI and local Ollama inference.
It is a **local LLM demonstration**, not an autonomous agent: there is no tool
execution, planning loop, or retrieval. It makes no cloud LLM API requests.

## Requirements

- Docker with Docker Compose (recommended) **or** Python 3.11+ and local Ollama
- Enough disk space and RAM to run your chosen Ollama model
- An internet connection for the initial Docker-image/model download

## Quick start: Docker

```bash
git clone https://github.com/kakarot987/first-local-ai-agent-ollama.git
cd first-local-ai-agent-ollama
bash run.sh
```

Open **http://localhost:7860**. The script starts Ollama, waits for it,
downloads the Mistral model inside the Ollama service, and then starts Gradio.

To start manually:

```bash
docker compose up -d ollama
docker compose exec -T ollama ollama pull mistral
docker compose up --build -d agent
docker compose logs -f agent
```

**Important:** `docker compose up` alone does not download the Mistral model.
Use `bash run.sh` or explicitly pull the model first. First inference may be
slower while the model loads. Logs: `docker compose logs -f agent ollama`.
Stop services with `docker compose down`. Data persists in the
`ollama_data` volume.

Compose points the UI to `http://ollama:11434` (the Docker service hostname),
and binds the Gradio server to `0.0.0.0` inside the container. Published
ports are restricted to the host loopback interface.

## Quick start: local Python

Install Ollama and pull the model:

```bash
ollama pull mistral
python -m venv .venv
source .venv/bin/activate    # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python agent_ui.py
```

Open **http://127.0.0.1:7860**. By default the UI connects to
`http://localhost:11434`; set `OLLAMA_HOST` to a different base URL if needed.
Use `OLLAMA_MODEL` to select another already-downloaded model, or
`OLLAMA_TIMEOUT` (seconds) to adjust request timeout.

### Optional FastAPI endpoint

```bash
uvicorn agent:app --host 127.0.0.1 --port 8000
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain transformers briefly"}'
```

The Docker image runs only the Gradio UI. The FastAPI module is a separate
local entry point.

## Testing

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests mock HTTP requests; a running Ollama service is not required.

## Architecture

User → Gradio UI (or FastAPI) → shared Python HTTP client → Ollama API → model

The app handles connection failures, timeouts, non-2xx HTTP responses,
malformed JSON, and empty responses. It does not implement chat memory.

## License

No license file is currently included. Add an explicit LICENSE if you plan
to permit reuse under a particular license.
