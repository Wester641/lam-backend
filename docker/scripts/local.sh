#!/bin/bash

set -euo pipefail

echo "🚀 Starting FastAPI app with Uvicorn..."
echo "📂 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"

# Rename .env.local to .env (for pydantic settings)
if [ -f ".env.local" ]; then
  echo "🔁 Copying content of .env.local to .env"
  cp .env.local .env
fi

# Run the original command passed to the container
exec "$@"
