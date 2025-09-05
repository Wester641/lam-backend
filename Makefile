.ONESHELL:
# Compose commands

create-db:
	@if [ ! -f ecommerce.db ]; then \
		echo "Creating database file..."; \
		touch ecommerce.db; \
		echo "Database file 'ecommerce.db' created."; \
	else \
		echo "Database file 'ecommerce.db' already exists."; \
	fi

compose-up:create-db
	docker compose -f docker/docker-compose.local.yml up --build -d

compose-down:
	docker compose -f docker/docker-compose.local.yml down

compose-dev-up:create-db
	docker compose -f docker/docker-compose.dev.yml up --build -d

compose-dev-down:
	docker compose -f docker/docker-compose.dev.yml down

makemigrations:
	@echo "Running migrations..."
	alembic revision --autogenerate -m "Migration"

migrate:
	@echo "Running migrations..."
	alembic upgrade head

run-dev-server:migrate
	@echo "Running from $(shell pwd)"
	python -m app.core.servers.uvicorn.run

run-server:migrate
	@echo "Running from $(shell pwd)"
	python -m app.core.servers.gunicorn.run