import logging
import os
from logging.handlers import RotatingFileHandler

from app.config.settings import LOG_LEVEL
from app.utils.path_manager import PathManager

LOGGER_NAME = "visionparse"
_CONFIGURED = False


def setup_logger():
    global _CONFIGURED

    logger = logging.getLogger(LOGGER_NAME)

    if _CONFIGURED:
        return logger

    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    logger.setLevel(level)
    logger.propagate = False

    # pasta segura para escrita do usuário
    log_dir = PathManager.output()
    log_file = os.path.join(log_dir, "visionparse.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    _CONFIGURED = True
    return logger


def get_logger(module_name=None):
    setup_logger()

    if module_name:
        return logging.getLogger(f"{LOGGER_NAME}.{module_name}")

    return logging.getLogger(LOGGER_NAME)