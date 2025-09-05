# ─────────────────────────────────────────────
# 🚧 Stage 1: Dependencies and build environment
# ─────────────────────────────────────────────

# Set the base image to Python 3.11 slim version
FROM python:3.11-bullseye AS dependencies

# Set the PYTHONUNBUFFERED environment variable to 1
ENV PYTHONUNBUFFERED 1

# Install apt packages with additional cleanup
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache -U pip setuptools \
    && rm -rf /root/.cache/pip \
    && pip install poetry

ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml and poetry.lock and environmental files to /opt/api/
COPY pyproject.toml poetry.lock .env.local /opt/api/

# Set the working directory to /opt/api/
WORKDIR /opt/api/

# Configure Poetry and install project dependencies (main only)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-cache --no-ansi --no-interaction --only main \
    && poetry cache clear pypi --all

# Copy the entrypoint script to /opt/docker/
COPY ./docker/scripts/local.sh /opt/docker/entrypoint.sh

# Change permissions of the entrypoint script
RUN chmod +x /opt/docker/entrypoint.sh

# ─────────────────────────────────────────────
# 🐳 Stage 2: Final runtime
# ─────────────────────────────────────────────
# Create a final stage
FROM dependencies AS final

# Copy the entire source directory to /opt/api/
COPY ./app /opt/api/app
COPY ./Makefile /opt/api/

# Set the entrypoint command to run the entrypoint script
ENTRYPOINT ["/opt/docker/entrypoint.sh"]
