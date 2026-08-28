import logging

from app.cli.menu import run
from app.database.init_db import initialize_database
from app.logging_config import configure_logging


logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()

    logger.info("CareerTrack application starting.")

    initialize_database()
    run()

    logger.info("CareerTrack application stopped.")


if __name__ == "__main__":
    main()
