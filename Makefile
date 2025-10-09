.ONESHELL:

# Docker Compose команды
compose-up:
	docker compose up --build -d

compose-down:
	docker compose down

compose-restart:
	docker compose restart

compose-logs:
	docker compose logs -f

compose-logs-api:
	docker compose logs -f api

compose-logs-db:
	docker compose logs -f db

# Очистка всех данных (ВНИМАНИЕ: удалит базу данных!)
compose-clean:
	docker compose down -v
	docker volume rm lnm-backend_postgres_data 2>/dev/null || true

# База данных
db-shell:
	docker compose exec db psql -U ecommerce_user -d ecommerce_db

db-backup:
	docker compose exec db pg_dump -U ecommerce_user ecommerce_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore:
	@read -p "Enter backup file path: " file; \
	docker compose exec -T db psql -U ecommerce_user -d ecommerce_db < $$file

# Миграции
makemigrations:
	@echo "Creating new migration..."
	docker compose exec api alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrate:
	@echo "Applying migrations..."
	docker compose exec api alembic upgrade head

migrate-down:
	@echo "Rolling back last migration..."
	docker compose exec api alembic downgrade -1

migration-history:
	docker compose exec api alembic history

# API команды
api-shell:
	docker compose exec api /bin/bash

api-restart:
	docker compose restart api

# Разработка
dev-setup:
	cp .env.example .env
	@echo "Please edit .env file with your settings"

dev-run:
	python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Тесты
test:
	docker compose exec api pytest

test-cov:
	docker compose exec api pytest --cov=app --cov-report=html

# Проверка статуса
status:
	docker compose ps
	@echo "\n=== Database Status ==="
	docker compose exec db pg_isready -U ecommerce_user -d ecommerce_db

# Полная пересборка
rebuild:
	docker compose down
	docker compose build --no-cache
	docker compose up -d
	sleep 10
	docker compose exec api alembic upgrade head

# Помощь
help:
	@echo "Available commands:"
	@echo "  compose-up          - Start all services"
	@echo "  compose-down        - Stop all services"
	@echo "  compose-restart     - Restart all services"
	@echo "  compose-logs        - Show all logs"
	@echo "  compose-logs-api    - Show API logs"
	@echo "  compose-logs-db     - Show database logs"
	@echo "  compose-clean       - Remove all data (WARNING: deletes database!)"
	@echo ""
	@echo "  db-shell            - Open PostgreSQL shell"
	@echo "  db-backup           - Create database backup"
	@echo "  db-restore          - Restore database from backup"
	@echo ""
	@echo "  makemigrations      - Create new migration"
	@echo "  migrate             - Apply migrations"
	@echo "  migrate-down        - Rollback last migration"
	@echo "  migration-history   - Show migration history"
	@echo ""
	@echo "  api-shell           - Open API container shell"
	@echo "  api-restart         - Restart API service"
	@echo ""
	@echo "  status              - Show services status"
	@echo "  rebuild             - Full rebuild (no cache)"
	@echo "  help                - Show this help"

# Для игнорирования аргументов после makemigrations
%:
	@: