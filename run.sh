#!/usr/bin/env bash
set -euo pipefail

echo "Starting Ollama service..."
docker compose up -d ollama
echo "Waiting for Ollama to become ready..."
for attempt in $(seq 1 30); do
  if docker compose exec -T ollama ollama list >/dev/null 2>&1; then
    break
  fi
  if [ "$attempt" = 30 ]; then
    echo "Ollama did not become ready." >&2
    exit 1
  fi
  sleep 2
done

MODEL="${OLLAMA_MODEL:-mistral}"
echo "Pulling model: $MODEL"
docker compose exec -T ollama ollama pull "$MODEL"
echo "Starting Gradio..."
docker compose up --build -d agent
echo "Visit http://localhost:7860"
