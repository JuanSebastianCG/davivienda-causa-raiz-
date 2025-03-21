from pydantic import BaseModel


class LogConfig(BaseModel):
    """Config for logging"""

    LOG_NAME: str = "causa_raiz"
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(message)s"
    LOG_FILE: str = "app.log"
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOG_NAME: {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    }
