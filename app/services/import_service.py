import csv
from pathlib import Path

from app.services.application_service import (
    ApplicationService,
)


class ImportService:
    def __init__(
        self,
        application_service: ApplicationService,
    ) -> None:
        self.application_service = application_service

    def import_applications_from_csv(
        self,
        file_path: str,
    ) -> list:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(
            path,
            newline="",
            encoding="utf-8",
        ) as file:
            return list(csv.DictReader(file))
