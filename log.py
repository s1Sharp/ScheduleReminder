import logging
from config import LOG_FILE_NAME


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(threadName)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_NAME, "w", "utf-8"),
            logging.StreamHandler()
        ]
    )
