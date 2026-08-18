import csv
from pathlib import Path

from app.services.application_service import (
    ApplicationService,
)
from app.services.interview_service import (
    InterviewService,
)


class ExportService:
    def __init__(
        self,
        application_service: (
            ApplicationService | None
        ) = None,
        interview_service: (
            InterviewService | None
        ) = None,
    ) -> None:
        self.application_service = (
            application_service
        )

        self.interview_service = (
            interview_service
        )

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

    def export_interviews_to_csv(
        self,
    ) -> str:
        interviews = (
            self.interview_service
            .get_interviews()
        )

        export_path = Path(
            "exports/interviews.csv"
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
                    "Application ID",
                    "Interview Date",
                    "Interview Type",
                    "Status",
                    "Notes",
                ]
            )

            for interview in interviews:
                writer.writerow(
                    [
                        interview.application_id,
                        interview.scheduled_at,
                        interview.interview_type,
                        interview.status,
                        interview.notes or "",
                    ]
                )

        return str(export_path)