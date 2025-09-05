from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

from pydantic import BaseModel


class GunicornSettings(BaseModel):
    """Configuration for Gunicorn server settings."""

    HOST: str = "0.0.0.0"  # noqa: S104
    PORT: int = 8000
    WORKERS: int = 1
    TIMEOUT: int = 900


class UnicornSettings(BaseModel):
    """Configuration for Uvicorn server settings."""

    HOST: str = "0.0.0.0"  # noqa: S104
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = True


class ServersSettings(BaseModel):
    """Aggregate settings for both Gunicorn and Uvicorn servers."""

    GUNICORN: GunicornSettings = GunicornSettings()
    UVICORN: UnicornSettings = UnicornSettings()


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
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:3001",
    ]

    # Файлы
    upload_dir: str = "uploads"
    max_file_size: int = 5242880  # 5MB

    servers: ServersSettings = ServersSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


# Глобальная конфигурация
settings = Settings()  # type: ignore
