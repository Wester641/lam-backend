#!/bin/bash

set -euo pipefail

echo "🚀 Starting FastAPI app with Uvicorn..."
echo "📂 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"

# Rename .env.dev to .env (for pydantic settings)
if [ -f ".env.dev" ]; then
  echo "🔁 Copying content of .env.dev to .env"
  cp .env.dev .env
fi

# Start the development server using make command
echo "🚀 Starting development server..."
make run-server

# Run the original command passed to the container
exec "$@"
