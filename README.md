# E-commerce Backend API

A FastAPI-based e-commerce backend with SQLite database and synchronous operations.

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry

### Installation

```bash
# Clone and install dependencies
poetry install

# Copy environment configuration
cp .env.local .env
```

## Database

The application uses SQLite for simplicity and portability. Database file: `ecommerce.db`

### Migrations

```bash
# Create new migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head
```

## Docker Deployment

### Local
```bash
make compose-up
```

### Development
```bash
make compose-dev-up
```

## API Documentation

- Swagger UI: `http://localhost:8010/docs`
- ReDoc: `http://localhost:8010/redoc`

