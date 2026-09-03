from datetime import UTC, date, datetime
from typing import cast

from app.database.connection import SessionLocal
from app.database.models.application import ApplicationDB
from app.models.application import (
    ApplicationStatus,
    ApplicationType,
)
from app.services.application_service import ApplicationService
from app.services.export_service import ExportService
from app.services.follow_up_service import FollowUpService
from app.services.import_service import ImportService
from app.services.interview_service import InterviewService


def add_application() -> None:
    print("\n--- Add Application ---")

    try:
        company_id = int(input("Company ID: ").strip())
    except ValueError:
        print("Company ID must be a number.")
        return

    position = input("Position: ").strip()

    print("\nSelect application type:")

    application_types = list(ApplicationType)

    for index, application_type_option in enumerate(
        application_types,
        start=1,
    ):
        print(f"{index}. {application_type_option.value}")

    application_type_choice = input("Application type: ").strip()

    application_type = None

    try:
        application_type_index = int(application_type_choice) - 1

        if 0 <= application_type_index < len(application_types):
            application_type = application_types[application_type_index].value

    except ValueError:
        choice_normalized = application_type_choice.strip().lower()

        for application_type_option in application_types:
            if application_type_option.value.lower() == choice_normalized:
                application_type = application_type_option.value
                break

    if application_type is None:
        print("Invalid application type selection.")
        return

    date_applied = input("Date applied (YYYY-MM-DD): ").strip()

    print("\nSelect application status:")

    statuses = list(ApplicationStatus)

    for index, application_status in enumerate(
        statuses,
        start=1,
    ):
        print(f"{index}. {application_status.value}")

    status_choice = input("Status: ").strip()

    status = None

    try:
        status_index = int(status_choice) - 1

        if 0 <= status_index < len(statuses):
            status = statuses[status_index].value

    except ValueError:
        choice_normalized = status_choice.strip().lower()

        for status_option in statuses:
            if status_option.value.lower() == choice_normalized:
                status = status_option.value
                break

    if status is None:
        print("Invalid status selection.")
        return

    try:
        parsed_date = date.fromisoformat(date_applied)

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        try:
            application = service.create_application(
                company_id=company_id,
                position=position,
                application_type=(application_type),
                date_applied=parsed_date,
                status=status,
            )

            print("\nApplication created successfully!")

            print(f"Application ID: {application.id}")

        except ValueError as error:
            print(f"\nError: {error}")


def list_applications() -> None:
    print("\n--- Applications ---")

    with SessionLocal() as session:
        service = ApplicationService(session)

        applications = service.get_applications()

        if not applications:
            print("No applications found.")
            return

        for application in applications:
            print(
                f"[{application.id}] "
                f"{application.position} | "
                f"Company ID: {application.company_id} | "
                f"Type: {application.application_type} | "
                f"Status: {application.status} | "
                f"Applied: {application.date_applied}"
            )


def sort_applications() -> None:
    print("\n--- Sort Applications ---")
    print("1. Date (Newest First)")
    print("2. Position (A-Z)")

    choice = input("Choose sorting option: ").strip()

    if choice == "1":
        field = "date"
        title = "Applications (Newest First)"
    elif choice == "2":
        field = "position"
        title = "Applications (Position A-Z)"
    else:
        print("Invalid sorting option.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        applications = service.get_sorted_applications(field)

        print(f"\n--- {title} ---")

        if not applications:
            print("No applications found.")
            return

        for application in applications:
            print(
                f"[{application.id}] "
                f"{application.position} | "
                f"Company ID: {application.company_id} | "
                f"Type: {application.application_type} | "
                f"Status: {application.status} | "
                f"Applied: {application.date_applied}"
            )


def view_application() -> None:
    print("\n--- View Application ---")

    try:
        application_id = int(input("Application ID: ").strip())
    except ValueError:
        print("Application ID must be a number.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        application = service.get_application(application_id)

        if application is None:
            print("Application not found.")
            return

        print("\nApplication Details")
        print("-" * 35)
        print(f"ID:             {application.id}")
        print(
            f"Company:        "
            f"{application.company.name if application.company else 'N/A'}"
        )
        print(f"Position:       {application.position}")
        print(f"Type:            {application.application_type}")
        print(f"Status:          {application.status}")
        print(f"Date Applied:   {application.date_applied}")
        print(f"Location:       {application.location or 'N/A'}")
        print(f"Deadline:       {application.deadline or 'N/A'}")
        print(f"Job URL:        {application.job_url or 'N/A'}")
        print(f"Notes:          {application.notes or 'N/A'}")
        print("-" * 35)


def update_application() -> None:
    print("\n--- Update Application ---")

    try:
        application_id = int(input("Application ID: ").strip())
    except ValueError:
        print("Application ID must be a number.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        application = service.get_application(application_id)

        if application is None:
            print("Application not found.")
            return

        print("\nPress Enter to keep the current value.")

        position = input(f"Position [{application.position}]: ").strip()

        status = input(f"Status [{application.status}]: ").strip()

        location = input(f"Location [{application.location or 'N/A'}]: ").strip()

        deadline = input(
            f"Deadline [{application.deadline or 'N/A'}] (YYYY-MM-DD): "
        ).strip()

        job_url = input(f"Job URL [{application.job_url or 'N/A'}]: ").strip()

        notes = input(f"Notes [{application.notes or 'N/A'}]: ").strip()

        parsed_deadline = None

        if deadline:
            try:
                parsed_deadline = date.fromisoformat(deadline)
            except ValueError:
                print("Invalid deadline. Use YYYY-MM-DD.")
                return

        try:
            updated = service.update_application(
                application_id=application_id,
                position=position if position else None,
                status=status if status else None,
                location=location if location else None,
                deadline=parsed_deadline,
                job_url=job_url if job_url else None,
                notes=notes if notes else None,
            )

            if updated is None:
                print("Application not found.")
                return

            print("\nApplication updated successfully!")

        except ValueError as error:
            print(f"\nError: {error}")


def search_applications() -> None:
    print("\n--- Search Applications ---")

    query = input("Search by position: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        applications = service.search_applications(query)

        if not applications:
            print("No applications found.")
            return

        print(f"\nSearch results for '{query}':")
        print("-" * 60)

        for application in applications:
            print(
                f"[{application.id}] "
                f"{application.position} | "
                f"Company ID: {application.company_id} | "
                f"Status: {application.status}"
            )

        print("-" * 60)


def filter_applications() -> None:
    print("\n--- Filter Applications ---")

    print("\nLeave a field empty to ignore that filter.")

    status = input("Status (Applied/Interview/Rejected/etc.): ").strip()

    application_type = input("Application type (Full-time/Internship/etc.): ").strip()

    company_id_input = input("Company ID: ").strip()

    company_id = None

    if company_id_input:
        try:
            company_id = int(company_id_input)
        except ValueError:
            print("Company ID must be a number.")
            return

    if not status and not application_type and company_id is None:
        print("Please provide at least one filter.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        applications = service.filter_applications(
            status=status or None,
            application_type=application_type or None,
            company_id=company_id,
        )

        if not applications:
            print("\nNo applications found.")
            return

        print("\nFiltered Applications")
        print("-" * 60)

        for application in applications:
            print(
                f"[{application.id}] "
                f"{application.position} | "
                f"Company ID: {application.company_id} | "
                f"Type: {application.application_type} | "
                f"Status: {application.status}"
            )

        print("-" * 60)
        print(f"Total results: {len(applications)}")


def delete_application() -> None:
    print("\n--- Delete Application ---")

    try:
        application_id = int(input("Application ID: ").strip())
    except ValueError:
        print("Application ID must be a number.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        application = service.get_application(application_id)

        if application is None:
            print("Application not found.")
            return

        print("\nApplication to delete:")
        print(f"Position: {application.position}")
        print(f"Status:   {application.status}")

        confirmation = (
            input("Are you sure you want to delete this application? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        deleted = service.delete_application(application_id)

        if deleted:
            print("\nApplication deleted successfully!")
        else:
            print("Application not found.")


def show_dashboard() -> None:
    print("\n--- CareerTrack Dashboard ---")

    with SessionLocal() as session:
        service = ApplicationService(session)

        interview_service = InterviewService(session)

        follow_up_service = FollowUpService(session)

        statistics = service.get_dashboard_statistics()

        monthly_applications = service.get_monthly_application_counts()
        location_statistics = service.get_location_statistics()
        interview_statistics = interview_service.get_interview_statistics()

        interview_analytics = interview_service.get_interview_analytics()

        follow_up_statistics = follow_up_service.get_follow_up_statistics()

        upcoming_follow_ups = follow_up_service.get_upcoming_follow_ups()

        upcoming_interviews = interview_service.get_upcoming_interviews()
        this_week_interviews = interview_service.get_this_week_interviews()
        total = statistics["total"]
        total_companies = statistics["total_companies"]
        success_rate = statistics["success_rate"]
        by_status = statistics["by_status"]

        by_application_type = statistics["by_application_type"]

        by_company = statistics["by_company"]
        # Get recent applications and upcoming deadlines
        recent_applications = service.get_recent_applications()

        upcoming_deadlines = service.get_upcoming_deadlines(
            today=datetime.now(UTC).date(),
        )

        print("\nTotal Applications")
        print("-" * 35)
        print(total)

        print("\nTotal Companies")
        print("-" * 35)
        print(total_companies)

        print("\nSuccess Rate")
        print("-" * 35)
        print(f"{success_rate:.1f}%")

        print("\nApplications by Status")
        print("-" * 35)

        if by_status:
            for status, count in sorted(by_status.items()):
                print(f"{status}: {count}")
        else:
            print("No applications found.")

        print("\nApplications by Type")
        print("-" * 35)

        if by_application_type:
            for application_type, count in sorted(by_application_type.items()):
                print(f"{application_type}: {count}")
        else:
            print("No applications found.")

        print("\nApplications by Company")
        print("-" * 35)

        if by_company:
            for company, count in sorted(by_company.items()):
                print(f"{company}: {count}")
        else:
            print("No applications found.")

        print("\nApplications by Month")
        print("-" * 35)

        if monthly_applications:
            for month, count in sorted(monthly_applications.items()):
                print(f"{month}: {count}")
        else:
            print("No applications found.")

        print("-" * 35)

        print("\nApplications by Location")
        print("-" * 35)

        if location_statistics:
            for location, count in sorted(location_statistics.items()):
                print(f"{location}: {count}")
        else:
            print("No applications found.")

        print("-" * 35)

        print("\nRecent Applications")
        print("-" * 35)

        if recent_applications:
            for application in recent_applications:
                company_name = (
                    application.company.name if application.company else "N/A"
                )

                print(
                    f"{application.position} | "
                    f"{company_name} | "
                    f"{application.date_applied}"
                )
        else:
            print("No applications found.")

        print("-" * 35)

        print("\nUpcoming Deadlines")
        print("-" * 60)

        if upcoming_deadlines:
            for application in upcoming_deadlines:
                company_name = (
                    application.company.name if application.company else "N/A"
                )

                print(
                    f"{application.position} | "
                    f"{company_name} | "
                    f"Deadline: {application.deadline} | "
                    f"Status: {application.status}"
                )
        else:
            print("No upcoming deadlines.")

        print("\nInterview Statistics")
        print("-" * 35)

        if interview_statistics:
            for status, count in sorted(interview_statistics.items()):
                print(f"{status}: {count}")
        else:
            print("No interviews found.")
        print("-" * 60)

        print("\nInterview Analytics")
        print("-" * 35)

        print(f"Total Interviews: {interview_analytics['total']}")

        print(f"Completed Interviews: {interview_analytics['completed']}")

        print(f"Cancelled Interviews: {interview_analytics['cancelled']}")

        print(f"Passed Interviews: {interview_analytics['passed']}")

        print(f"Failed Interviews: {interview_analytics['failed']}")

        print(f"Pending Interviews: {interview_analytics['pending']}")

        print(f"Online Interviews: {interview_analytics['online']}")

        print(f"Phone Interviews: {interview_analytics['phone']}")

        print(f"On-site Interviews: {interview_analytics['on_site']}")

        print("-" * 60)

        print("\nUpcoming Interviews")
        print("-" * 60)

        if upcoming_interviews:
            for interview in upcoming_interviews:
                if interview.application:
                    position = interview.application.position

                    company_name = (
                        interview.application.company.name
                        if interview.application.company
                        else "N/A"
                    )

                else:
                    position = "N/A"
                    company_name = "N/A"

                print(
                    f"{interview.scheduled_at} | "
                    f"{position} | "
                    f"{company_name} | "
                    f"{interview.interview_type}"
                )
        else:
            print("No upcoming interviews found.")

        print("-" * 60)

        print("\nInterviews This Week")
        print("-" * 60)

        if this_week_interviews:
            for interview in this_week_interviews:
                interview_application = cast(
                    "ApplicationDB | None",
                    getattr(interview, "application", None),
                )

                if interview_application:
                    position = interview_application.position

                    company = getattr(
                        interview_application,
                        "company",
                        None,
                    )

                    company_name = company.name if company else "N/A"

                else:
                    position = "N/A"
                    company_name = "N/A"

                print(f"{interview.scheduled_at} | {position} | {company_name}")
        else:
            print("No interviews scheduled this week.")
        print("-" * 60)
        print("\nFollow-Up Statistics")
        print("-" * 35)

        print(f"Total Follow-Ups: {follow_up_statistics['total']}")

        print(f"Completed Follow-Ups: {follow_up_statistics['completed']}")

        print(f"Pending Follow-Ups: {follow_up_statistics['pending']}")

        print("-" * 60)

        print("\nUpcoming Follow-Ups")
        print("-" * 60)

        if upcoming_follow_ups:
            for follow_up in upcoming_follow_ups:
                print(
                    f"{follow_up.follow_up_at} | "
                    f"Application ID: "
                    f"{follow_up.application_id} | "
                    f"{follow_up.note}"
                )
        else:
            print("No upcoming follow-ups.")

        print("-" * 60)


def export_applications() -> None:
    print("\n--- Export Applications ---")

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        exporter = ExportService(application_service)

        path = exporter.export_applications_to_csv()

        print(f"Applications exported to: {path}")


def import_applications() -> None:
    print("\n--- Import Applications ---")

    file_path = input("CSV file path: ").strip()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        importer = ImportService(application_service)

        try:
            rows = importer.import_applications_from_csv(file_path)

            print(f"Imported {len(rows)} applications.")

        except FileNotFoundError as error:
            print(error)
