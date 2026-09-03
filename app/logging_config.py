import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "career_track.log"


def configure_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)

    root_logger = logging.getLogger()

    # Avoid creating duplicate handlers if logging is configured
    # more than once during the application's lifetime.
    if root_logger.handlers:
        return

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
