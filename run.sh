#!/bin/bash

echo "🚀 Starting Local AI Agent..."

# Ensure the Ollama container is running before pulling the model
echo "🔍 Checking if Ollama container is running..."
if ! docker ps --format '{{.Names}}' | grep -q '^ollama-1$'; then
  echo "❌ Ollama container 'ollama-1' is not running. Starting Docker Compose first..."
  docker-compose up -d --build
  sleep 5  # Give it a moment to initialize
else
  echo "✅ Ollama container is already running."
fi

# Pull the Mistral model inside the container
echo "📦 Pulling Mistral model inside 'ollama-1' container..."
docker exec ollama-1 ollama pull mistral

# Launch all containers (if not already running)
echo "🚀 Launching remaining containers..."
docker-compose up --build
