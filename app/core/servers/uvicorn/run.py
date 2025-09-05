"""Main Uvicorn Application Entry Point."""

__all__ = ("main",)

import uvicorn

from app.config import settings


def main() -> None:
    """Run the Uvicorn application with FastAPI app and configuration options."""
    uvicorn.run(
        "app.main:app",
        host=settings.servers.UVICORN.HOST,
        port=settings.servers.UVICORN.PORT,
        reload=settings.servers.UVICORN.RELOAD,
        workers=settings.servers.UVICORN.WORKERS,
    )


if __name__ == "__main__":
    main()
