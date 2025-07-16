from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Основные настройки
    app_name: str = "E-commerce Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # База данных
    database_url: str
    
    # Безопасность
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:3001"]
    
    # Файлы
    upload_dir: str = "uploads"
    max_file_size: int = 5242880  # 5MB
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Глобальная конфигурация
settings = Settings()