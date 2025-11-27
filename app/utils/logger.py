import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import LOGS_DIR

def get_logger(name="voice_to_text"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(LOGS_DIR / f"{name}.log", maxBytes=2_000_000, backupCount=3)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
    logger.addHandler(fh)

    return logger
