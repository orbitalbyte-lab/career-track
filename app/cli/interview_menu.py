from datetime import datetime

from app.database.connection import SessionLocal
from app.models.interview import (
    Interview,
    InterviewOutcome,
    InterviewStatus,
    InterviewType,
)
from app.services.interview_service import InterviewService
from app.services.export_service import ExportService


def add_interview() -> None:
    print("\n--- Add Interview ---")

    while True:
        try:
            application_id = int(
                input("Application ID: ").strip()
            )
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            scheduled_at = datetime.fromisoformat(
                input(
                    "Interview date and time (YYYY-MM-DD HH:MM): "
                ).strip()
            )
            break
        except ValueError:
            print("Please enter the date as YYYY-MM-DD HH:MM.")

    while True:
        try:
            interview_type = InterviewType(
                input(
                    "Interview type (Online/Phone/On-site): "
                ).strip().title()
            )
            break
        except ValueError:
            print("Please choose Online, Phone, or On-site.")

    outcome = InterviewOutcome.PENDING

    notes = (
        input("Notes (optional): ").strip()
        or None
    )

    interview = Interview(
        application_id=application_id,
        scheduled_at=scheduled_at,
        interview_type=interview_type,
        outcome=outcome,
        notes=notes,
    )

    with SessionLocal() as session:
        interview_service = InterviewService(session)
        interview_service.create_interview(interview)

    print("Interview scheduled successfully.")


def list_interviews() -> None:
    print("\n--- Interviews ---")

    with SessionLocal() as session:
        interview_service = InterviewService(session)
        interviews = interview_service.get_interviews()

        if not interviews:
            print("No interviews found.")
            return

        for interview in interviews:
            print(
                f"Interview ID: {interview.id} | "
                f"Application ID: {interview.application_id} | "
                f"Type: {interview.interview_type} | "
                f"Status: {interview.status} | "
                f"Date: {interview.scheduled_at}"
            )


def view_interview() -> None:
    print("\n--- Interview Details ---")

    try:
        interview_id = int(input("Interview ID: ").strip())
    except ValueError:
        print("Interview ID must be a number.")
        return

    with SessionLocal() as session:
        interview_service = InterviewService(session)
        interview = interview_service.get_interview(interview_id)

        if interview is None:
            print("Interview not found.")
            return

        application = getattr(interview, "application", None)

        company = (
            getattr(application, "company", None)
            if application
            else None
        )

        print(f"\nInterview ID: {interview.id}")
        print(f"Application ID: {interview.application_id}")
        print(f"Company: {company.name if company else 'N/A'}")
        print(
            f"Position: "
            f"{application.position if application else 'N/A'}"
        )
        print(f"Date: {interview.scheduled_at}")
        print(f"Type: {interview.interview_type}")
        print(f"Status: {interview.status}")
        print(f"Outcome: {interview.outcome}")
        print(f"Notes: {interview.notes or ''}")


def update_interview() -> None:
    print("\n--- Update Interview ---")

    try:
        interview_id = int(input("Interview ID: ").strip())
    except ValueError:
        print("Please enter a valid ID.")
        return

    print("Scheduled | Completed | Canceled")

    try:
        status = InterviewStatus(
            input("New status: ").strip().title()
        )
    except ValueError:
        print("Invalid status.")
        return

    print("Pending | Passed | Failed")

    try:
        outcome = InterviewOutcome(
            input("Interview outcome: ").strip().title()
        )
    except ValueError:
        print("Invalid outcome.")
        return

    with SessionLocal() as session:
        interview_service = InterviewService(session)

        interview = interview_service.update_interview(
            interview_id,
            status.value,
            outcome.value,
        )

        if interview is None:
            print("Interview not found.")
            return

    print("Interview updated successfully.")


def delete_interview() -> None:
    print("\n--- Delete Interview ---")

    try:
        interview_id = int(input("Interview ID: ").strip())
    except ValueError:
        print("Please enter a valid ID.")
        return

    with SessionLocal() as session:
        interview_service = InterviewService(session)

        deleted = interview_service.delete_interview(
            interview_id
        )

        if deleted is None:
            print("Interview not found.")
            return

    print("Interview deleted successfully.")


def search_interviews() -> None:
    print("\n--- Search Interviews ---")

    query = input("Search: ").strip()

    with SessionLocal() as session:
        interview_service = InterviewService(session)

        interviews = interview_service.search_interviews(query)

        if not interviews:
            print("No interviews found.")
            return

        for interview in interviews:
            print(
                f"Interview ID: {interview.id} | "
                f"Application ID: {interview.application_id} | "
                f"Type: {interview.interview_type} | "
                f"Status: {interview.status}"
            )


def filter_interviews() -> None:
    print("\n--- Filter Interviews ---")

    status = input(
        "Status (Scheduled/Completed/Cancelled): "
    ).strip()

    with SessionLocal() as session:
        interview_service = InterviewService(session)

        interviews = interview_service.get_interviews_by_status(
            status
        )

        if not interviews:
            print("No interviews found.")
            return

        for interview in interviews:
            print(
                f"Interview ID: {interview.id} | "
                f"Application ID: {interview.application_id} | "
                f"Type: {interview.interview_type} | "
                f"Status: {interview.status}"
            )


def sort_interviews() -> None:
    print("\n--- Sort Interviews ---")
    print("1. Date (Newest First)")
    print("2. Interview Type (A-Z)")

    choice = input("Choose sorting option: ").strip()

    if choice == "1":
        field = "date"
        title = "Interviews (Newest First)"
    elif choice == "2":
        field = "type"
        title = "Interviews (Type A-Z)"
    else:
        print("Invalid sorting option.")
        return

    with SessionLocal() as session:
        interview_service = InterviewService(session)

        interviews = interview_service.get_sorted_interviews(field)

        print(f"\n--- {title} ---")

        if not interviews:
            print("No interviews found.")
            return

        for interview in interviews:
            print(
                f"[{interview.id}] "
                f"Application ID: {interview.application_id} | "
                f"Type: {interview.interview_type} | "
                f"Status: {interview.status} | "
                f"Date: {interview.scheduled_at}"
            )
def export_interviews() -> None:
    print("\n--- Export Interviews ---")

    with SessionLocal() as session:
        interview_service = (
            InterviewService(session)
        )

        exporter = ExportService(
            interview_service=(
                interview_service
            )
        )

        path = (
            exporter.export_interviews_to_csv()
        )

        print(
            f"Interviews exported to: {path}"
        )
