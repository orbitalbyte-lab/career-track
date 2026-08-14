import csv
from pathlib import Path

from app.services.application_service import ApplicationService


class ExportService:
    def __init__(
        self,
        application_service: ApplicationService,
    ) -> None:
        self.application_service = application_service

    def export_applications_to_csv(
        self,
    ) -> str:
        applications = (
            self.application_service
            .get_applications()
        )

        export_path = Path(
            "exports/applications.csv"
        )

        export_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            export_path,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    "Company",
                    "Position",
                    "Application Type",
                    "Status",
                    "Date Applied",
                    "Location",
                    "Deadline",
                    "Job URL",
                    "Notes",
                ]
            )

            for application in applications:
                writer.writerow(
                    [
                        (
                            application.company.name
                            if application.company
                            else "N/A"
                        ),
                        application.position,
                        application.application_type,
                        application.status,
                        application.date_applied,
                        application.location or "",
                        application.deadline or "",
                        application.job_url or "",
                        application.notes or "",
                    ]
                )

        return str(export_path)