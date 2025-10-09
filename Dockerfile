# ─────────────────────────────────────────────
# 🚧 Stage 1: Dependencies and build environment
# ─────────────────────────────────────────────
FROM python:3.11-bullseye AS dependencies

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    make \
    curl \
    libssl1.1 \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip setuptools \
    && pip install --no-cache-dir poetry

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /opt/app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main --no-interaction --no-ansi

# ─────────────────────────────────────────────
# 🐳 Stage 2: Final runtime
# ─────────────────────────────────────────────
FROM python:3.11-slim-bullseye AS final

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    libssl1.1 \
    libpq5 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY --from=dependencies /usr/local /usr/local

COPY app ./app

RUN mkdir -p /opt/app/uploads && chmod 755 /opt/app/uploads

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]