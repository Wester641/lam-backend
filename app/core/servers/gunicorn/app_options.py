"""Gunicorn Application Options Configuration."""


def get_app_options(
    host: str,
    port: int,
    timeout: int,
    workers: int,
    log_level: str,
) -> dict:
    """Return Gunicorn application options."""
    return {
        "accesslog": "-",
        "errorlog": "-",
        "bind": f"{host}:{port}",
        "loglevel": log_level,
        "timeout": timeout,
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
