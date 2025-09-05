"""Gunicorn Application Configuration."""

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    """Gunicorn application class to load FastAPI app and set configuration options."""

    def __init__(
        self,
        application: FastAPI,
        options: dict | None = None,
    ) -> None:
        """Initialize the Gunicorn application with FastAPI app and configuration options."""
        self.options = options or {}
        self.application = application
        super().__init__()

    def load(self) -> FastAPI:
        """Load the FastAPI application."""
        return self.application

    @property
    def config_options(self) -> dict:
        """Return the configuration options for Gunicorn."""
        return {
            # pair
            k: v
            # for each option
            for k, v in self.options.items()
            # not empty key / value
            if k in self.cfg.settings and v is not None  # type: ignore
        }

    def load_config(self) -> None:
        """Load the configuration options into Gunicorn."""
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)  # type: ignore
