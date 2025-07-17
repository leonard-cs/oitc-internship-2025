#!/bin/sh

echo "🚀 Starting Ollama server in background..."
ollama serve &

# Wait for the Ollama server to be up
echo "⏳ Waiting for Ollama to become responsive..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

echo "✅ Ollama is up. Pulling models..."

ollama pull phi3
ollama pull nomic-embed-text

echo "✅ Finished pulling models. Server is running..."

wait