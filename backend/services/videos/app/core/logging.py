import logging
import logging.handlers
import os

LOG_DIR = os.getenv("LOG_DIR", "/app/logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

_configured = False


def setup_logging() -> None:
    """Send app and uvicorn logs to both stdout and a rotating file under LOG_DIR.

    Uvicorn's "uvicorn" and "uvicorn.access" loggers have propagate=False,
    so the file handler has to be attached to them directly - attaching it
    only to the root logger would miss them. "uvicorn.error" is left out:
    it propagates into "uvicorn" by default, so adding the handler there
    too would log every uvicorn.error record twice.
    """
    global _configured
    if _configured:
        return
    _configured = True

    os.makedirs(LOG_DIR, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    for name in ("uvicorn", "uvicorn.access"):
        logging.getLogger(name).addHandler(file_handler)
