"""Main Gunicorn Application Entry Point."""

__all__ = ("main",)

from app.config import settings
from app.core.servers.gunicorn.app_options import get_app_options
from app.core.servers.gunicorn.application import Application
from app.main import app as fastapi_app


def main() -> None:
    """Run the Gunicorn application with FastAPI app and configuration options."""
    Application(
        application=fastapi_app,
        options=get_app_options(
            host=settings.servers.GUNICORN.HOST,
            port=settings.servers.GUNICORN.PORT,
            timeout=settings.servers.GUNICORN.TIMEOUT,
            workers=settings.servers.GUNICORN.WORKERS,
            log_level="INFO",
        ),
    ).run()


if __name__ == "__main__":
    main()
