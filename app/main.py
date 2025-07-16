from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.api.v1.api import api_router
from app.core.middleware import setup_middleware
from app.core.exceptions import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)

# Создание FastAPI приложения
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API для интернет-магазина",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка middleware
setup_middleware(app)

# Обработчики ошибок
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Подключение роутеров
app.include_router(api_router, prefix="/api/v1")

# Корневой эндпоинт
@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "E-commerce Backend API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Эндпоинт для проверки здоровья приложения
@app.get("/health")
async def health_check():
    """Проверка состояния приложения"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }

# Эндпоинт для получения информации о API
@app.get("/api/v1")
async def api_info():
    """Информация о API"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "categories": "/api/v1/categories",
            "brands": "/api/v1/brands", 
            "products": "/api/v1/products"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/api/v1/openapi.json"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )