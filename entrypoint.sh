#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

python << 'PYEOF'
import time
import sys
import os
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "ecommerce_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ecommerce_password123")
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce_db")

MAX_RETRIES = 30
RETRY_INTERVAL = 2

print(f"Connecting to: {DB_HOST}:{DB_PORT}/{DB_NAME} as {DB_USER}")

for attempt in range(1, MAX_RETRIES + 1):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            connect_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        print("✓ PostgreSQL is ready!")
        sys.exit(0)
    except Exception as e:
        if attempt < MAX_RETRIES:
            print(f"✗ Attempt {attempt}/{MAX_RETRIES} failed, retrying in {RETRY_INTERVAL}s...")
            time.sleep(RETRY_INTERVAL)
        else:
            print(f"✗ Failed after {MAX_RETRIES} attempts")
            print(f"Error: {e}")
            sys.exit(1)
PYEOF

echo "Running Alembic migrations..."
cd /opt/app

if [ ! -f "alembic.ini" ]; then
    echo "ERROR: alembic.ini not found in /opt/app"
    ls -la
    exit 1
fi

alembic -c alembic.ini upgrade head

echo "Migrations completed successfully!"

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
