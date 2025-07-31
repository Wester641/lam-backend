# E-commerce Backend API

Полнофункциональное REST API для интернет-магазина на FastAPI + PostgreSQL.

## 📋 Содержание

- [Быстрый старт](#-быстрый-старт)
- [Требования](#-требования)
- [Установка](#-установка)
- [Запуск проекта](#-запуск-проекта)
- [API документация](#-api-документация)
- [Структура проекта](#-структура-проекта)
- [Тестирование](#-тестирование)

## 🚀 Быстрый старт

```bash
# 1. Клонировать репозиторий.
git clone <repository-url>
cd backend

# 2. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить .env файл (см. ниже)
cp .env.example .env

# 5. Создать базу данных PostgreSQL
# 6. Запустить миграции
alembic upgrade head

# 7. Заполнить тестовыми данными (опционально)
python test_services.py

# 8. Запустить сервер
python run_server.py
```

**Готово!** API доступен по адресу: http://localhost:8000/docs

## ⚙️ Требования

- **Python**: 3.11+
- **PostgreSQL**: 12+
- **pip**: latest
- **Git**: latest

## 📦 Установка

### 1. Клонирование и настройка окружения

```bash
# Клонировать репозиторий
git clone <repository-url>
cd backend

# Создать виртуальное окружение
python3 -m venv venv

# Активировать виртуальное окружение
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Обновить pip
pip install --upgrade pip

# Установить зависимости
pip install -r requirements.txt
```

### 2. Установка PostgreSQL

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS (Homebrew)
```bash
brew install postgresql
brew services start postgresql
```

#### Windows
Скачайте и установите PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/

### 3. Создание базы данных

```bash
# Подключиться к PostgreSQL
sudo -u postgres psql  # Linux
psql postgres          # macOS/Windows

# В psql консоли выполнить:
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### 4. Конфигурация проекта

Создайте файл `.env` в корне проекта:

```env
# База данных
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ecommerce_db

# Настройки приложения
APP_NAME=E-commerce Backend
APP_VERSION=1.0.0
DEBUG=True

# CORS настройки (добавьте адреса вашего фронтенда)
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://localhost:3001"]

# Безопасность
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Загрузка файлов
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
```

**⚠️ Важно:** Замените `your_password` и `your-secret-key-change-in-production` на реальные значения!

### 5. Инициализация базы данных

```bash
# Создать миграции (если еще не создан)
alembic revision --autogenerate -m "Initial migration"

# Применить миграции
alembic upgrade head

# Проверить подключение к БД
python test_db.py
```

### 6. Заполнение тестовыми данными

```bash
# Создать тестовые категории, бренды и товары
python test_services.py
```

## 🏃 Запуск проекта

### Разработка

```bash
# Запуск сервера разработки
python run_server.py

# Или напрямую через uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Запуск production сервера
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Сервер будет доступен по адресу: **http://localhost:8000**

## 📚 API документация

После запуска сервера доступны следующие ресурсы:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

### Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/` | Информация о API |
| `GET` | `/health` | Проверка состояния |
| `GET` | `/api/v1/products` | Список товаров |
| `GET` | `/api/v1/products/{id}` | Товар по ID |
| `GET` | `/api/v1/products/featured` | Рекомендуемые товары |
| `GET` | `/api/v1/products/search?q=запрос` | Поиск товаров |
| `POST` | `/api/v1/products` | Создать товар |
| `PUT` | `/api/v1/products/{id}` | Обновить товар |
| `DELETE` | `/api/v1/products/{id}` | Удалить товар |
| `GET` | `/api/v1/categories` | Список категорий |
| `GET` | `/api/v1/categories/tree` | Дерево категорий |
| `POST` | `/api/v1/categories` | Создать категорию |
| `GET` | `/api/v1/brands` | Список брендов |
| `GET` | `/api/v1/brands/popular` | Популярные бренды |
| `POST` | `/api/v1/brands` | Создать бренд |

### Фильтрация товаров

```
GET /api/v1/products?category_id=1&brand_id=2&min_price=100&max_price=1000&in_stock=true
```

Доступные параметры:
- `category_id` - фильтр по категории
- `brand_id` - фильтр по бренду
- `min_price` - минимальная цена
- `max_price` - максимальная цена
- `in_stock` - только в наличии
- `featured` - только рекомендуемые
- `search` - поиск по названию
- `sort_by` - сортировка (price, created_at, title)
- `sort_order` - порядок (asc, desc)
- `skip` - пропустить записей
- `limit` - количество записей

## 🏗️ Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Основное FastAPI приложение
│   ├── config.py               # Конфигурация
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Подключение к БД
│   │   └── models.py          # SQLAlchemy модели
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py         # Pydantic схемы товаров
│   │   ├── category.py        # Схемы категорий
│   │   ├── brand.py           # Схемы брендов
│   │   └── common.py          # Общие схемы
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py            # Базовый репозиторий
│   │   ├── product.py         # Репозиторий товаров
│   │   ├── category.py        # Репозиторий категорий
│   │   └── brand.py           # Репозиторий брендов
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py # Бизнес-логика товаров
│   │   ├── category_service.py
│   │   └── brand_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # FastAPI зависимости
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py         # Главный роутер API v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── products.py    # Эндпоинты товаров
│   │           ├── categories.py  # Эндпоинты категорий
│   │           └── brands.py      # Эндпоинты брендов
│   └── core/
│       ├── __init__.py
│       ├── exceptions.py      # Обработка ошибок
│       └── middleware.py      # CORS и другие middleware
├── migrations/                # Alembic миграции
├── tests/                    # Тесты
├── requirements.txt          # Python зависимости
├── alembic.ini              # Конфигурация Alembic
├── .env                     # Переменные окружения
├── run_server.py            # Скрипт запуска сервера
├── test_db.py              # Тест подключения к БД
├── test_services.py        # Тест сервисов и заполнение данными
└── README.md               # Эта документация
```

## 🧪 Тестирование

### Проверка подключения к БД

```bash
python test_db.py
```

### Тестирование API

```bash
# Тест сервисов и создание тестовых данных
python test_services.py

# Тест API эндпоинтов (требует requests)
pip install requests
python test_api.py
```

### Примеры запросов с curl

```bash
# Получить все товары
curl http://localhost:8000/api/v1/products

# Получить товар по ID
curl http://localhost:8000/api/v1/products/1

# Поиск товаров
curl "http://localhost:8000/api/v1/products/search?q=Samsung"

# Создать категорию
curl -X POST "http://localhost:8000/api/v1/categories" \
     -H "Content-Type: application/json" \
     -d '{"name": "Ноутбуки", "description": "Категория ноутбуков"}'

# Создать товар
curl -X POST "http://localhost:8000/api/v1/products" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "iPhone 15 Pro",
       "description": "Новый iPhone",
       "sku": "IP15-PRO-001",
       "base_price": 999.99,
       "total_stock": 10,
       "category_id": 1,
       "brand_id": 1
     }'
```

## 🔧 Возможные проблемы и решения

### Ошибка подключения к PostgreSQL

```bash
# Проверить статус PostgreSQL
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS

# Перезапустить PostgreSQL
sudo systemctl restart postgresql  # Linux
brew services restart postgresql  # macOS
```

### Ошибка миграций

```bash
# Сбросить миграции (⚠️ удалит все данные)
alembic downgrade base
alembic upgrade head

# Создать новую миграцию
alembic revision --autogenerate -m "Your migration message"
```

### Ошибка зависимостей Python

```bash
# Переустановить зависимости
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Проблемы с CORS

Убедитесь что в `.env` файле указаны правильные адреса фронтенда:

```env
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи сервера
2. Убедитесь что PostgreSQL запущен
3. Проверьте настройки в `.env` файле
4. Запустите тесты: `python test_db.py`

## 🚀 Готово!

После успешной установки и запуска:

- API доступен по адресу: **http://localhost:8000**
- Документация: **http://localhost:8000/docs**
- Здоровье сервиса: **http://localhost:8000/health**

Удачной разработки! 🎉