# E-commerce Backend API

Полнофункциональное API для интернет-магазина на FastAPI + PostgreSQL.

## 📋 Содержание

- [Быстрый старт](#быстрый-старт)
- [Установка](#установка)
- [API документация](#api-документация)
- [Структура данных](#структура-данных)
- [Примеры запросов](#примеры-запросов)
- [Админ панель](#админ-панель)

## 🚀 Быстрый старт

1. **Клонируйте репозиторий**
2. **Запустите установку:** `./setup.sh` (или следуйте инструкции ниже)
3. **Откройте документацию:** http://localhost:8000/docs

## 📦 Установка

### Требования

- Python 3.11+
- PostgreSQL 12+
- pip

### Пошаговая установка

#### 1. Настройка окружения

```bash
# Создать виртуальное окружение
python3 -m venv venv

# Активировать (Linux/Mac)
source venv/bin/activate

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

#### 2. Настройка базы данных

**PostgreSQL установка:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (Homebrew)
brew install postgresql
brew services start postgresql

# Windows
# Скачать с https://www.postgresql.org/download/windows/
```

**Создание базы данных:**

```sql
-- Подключиться к PostgreSQL
psql -U postgres

-- Создать базу данных
CREATE DATABASE ecommerce_db;

-- Создать пользователя (опционально)
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
```

#### 3. Конфигурация

Создайте файл `.env` в корне проекта:

```env
# База данных
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ecommerce_db

# Настройки приложения
APP_NAME=E-commerce Backend
APP_VERSION=1.0.0
DEBUG=True

# CORS для фронтенда
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://localhost:3001"]

# Безопасность
SECRET_KEY=your-secret-key-change-in-production
```

#### 4. Инициализация БД

```bash
# Создать