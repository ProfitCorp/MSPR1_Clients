import logging
import os
import sys

def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout
    )

    # Réduire le bruit des bibliothèques tierces si besoin
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logging.getLogger("app")