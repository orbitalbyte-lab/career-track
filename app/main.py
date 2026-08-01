from app.cli.menu import run
from app.database.init_db import initialize_database


def main() -> None:
    initialize_database()
    run()


if __name__ == "__main__":
    main()