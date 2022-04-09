import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE_NAME


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(threadName)s] [%(levelname)s] %(message)s",
        handlers=[
            RotatingFileHandler(LOG_FILE_NAME, maxBytes=10 * 1024 * 1024, mode="w",
                                encoding="utf-8", backupCount=5),
            logging.StreamHandler()
        ]
    )
