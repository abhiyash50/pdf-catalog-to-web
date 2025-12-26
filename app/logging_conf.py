import logging
import logging.config
from typing import Any, Dict


LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        },
        "json": {
            "format": "{\"time\":\"%(asctime)s\",\"level\":\"%(levelname)s\",\"name\":\"%(name)s\",\"message\":\"%(message)s\"}",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)


__all__ = ["configure_logging", "LOGGING_CONFIG"]
