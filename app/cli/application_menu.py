from datetime import date

from app.database.connection import SessionLocal
from app.models.application import (
    ApplicationStatus,
    ApplicationType,
)
from app.services.application_service import ApplicationService


def add_application() -> None:
    print("\n--- Add Application ---")

    try:
        company_id = int(
            input("Company ID: ").strip()
        )
    except ValueError:
        print("Company ID must be a number.")
        return

    position = input(
        "Position: "
    ).strip()

    print("\nSelect application type:")

    application_types = list(ApplicationType)

    for index, application_type_option in enumerate(
        application_types,
        start=1,
    ):
        print(
            f"{index}. "
            f"{application_type_option.value}"
        )

    application_type_choice = input(
        "Application type: "
    ).strip()

    application_type = None

    try:
        application_type_index = (
            int(application_type_choice) - 1
        )

        if (
            0
            <= application_type_index
            < len(application_types)
        ):
            application_type = (
                application_types[
                    application_type_index
                ].value
            )

    except ValueError:
        choice_normalized = (
            application_type_choice
            .strip()
            .lower()
        )

        for application_type_option in (
            application_types
        ):
            if (
                application_type_option.value.lower()
                == choice_normalized
            ):
                application_type = (
                    application_type_option.value
                )
                break

    if application_type is None:
        print(
            "Invalid application type selection."
        )
        return

    date_applied = input(
        "Date applied (YYYY-MM-DD): "
    ).strip()

    print("\nSelect application status:")

    statuses = list(ApplicationStatus)

    for index, application_status in enumerate(
        statuses,
        start=1,
    ):
        print(
            f"{index}. "
            f"{application_status.value}"
        )

    status_choice = input(
        "Status: "
    ).strip()

    status = None

    try:
        status_index = (
            int(status_choice) - 1
        )

        if (
            0
            <= status_index
            < len(statuses)
        ):
            status = (
                statuses[
                    status_index
                ].value
            )

    except ValueError:
        choice_normalized = (
            status_choice
            .strip()
            .lower()
        )

        for status_option in statuses:
            if (
                status_option.value.lower()
                == choice_normalized
            ):
                status = (
                    status_option.value
                )
                break

    if status is None:
        print(
            "Invalid status selection."
        )
        return

    try:
        parsed_date = date.fromisoformat(
            date_applied
        )

    except ValueError:
        print(
            "Invalid date. Use YYYY-MM-DD."
        )
        return

    with SessionLocal() as session:
        service = ApplicationService(
            session
        )

        try:
            application = (
                service.create_application(
                    company_id=company_id,
                    position=position,
                    application_type=(
                        application_type
                    ),
                    date_applied=parsed_date,
                    status=status,
                )
            )

            print(
                "\nApplication created successfully!"
            )

            print(
                f"Application ID: "
                f"{application.id}"
            )

        except ValueError as error:
            print(
                f"\nError: {error}"
            )


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

    choice = input(
        "Choose sorting option: "
    ).strip()

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

        applications = (
            service.get_sorted_applications(field)
        )

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
        application_id = int(
            input("Application ID: ").strip()
        )
    except ValueError:
        print("Application ID must be a number.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        application = service.get_application(
            application_id
        )

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
        application_id = int(
            input("Application ID: ").strip()
        )
    except ValueError:
        print("Application ID must be a number.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        application = service.get_application(
            application_id
        )

        if application is None:
            print("Application not found.")
            return

        print("\nPress Enter to keep the current value.")

        position = input(
            f"Position [{application.position}]: "
        ).strip()

        status = input(
            f"Status [{application.status}]: "
        ).strip()

        location = input(
            f"Location [{application.location or 'N/A'}]: "
        ).strip()

        deadline = input(
            f"Deadline [{application.deadline or 'N/A'}] "
            "(YYYY-MM-DD): "
        ).strip()

        job_url = input(
            f"Job URL [{application.job_url or 'N/A'}]: "
        ).strip()

        notes = input(
            f"Notes [{application.notes or 'N/A'}]: "
        ).strip()

        parsed_deadline = None

        if deadline:
            try:
                parsed_deadline = date.fromisoformat(
                    deadline
                )
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

    query = input(
        "Search by position: "
    ).strip()

    if not query:
        print("Search query cannot be empty.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        applications = service.search_applications(
            query
        )

        if not applications:
            print("No applications found.")
            return

        print(
            f"\nSearch results for '{query}':"
        )
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

    status = input(
        "Status (Applied/Interview/Rejected/etc.): "
    ).strip()

    application_type = input(
        "Application type (Full-time/Internship/etc.): "
    ).strip()

    company_id_input = input(
        "Company ID: "
    ).strip()

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
        application_id = int(
            input("Application ID: ").strip()
        )
    except ValueError:
        print("Application ID must be a number.")
        return

    with SessionLocal() as session:
        service = ApplicationService(session)

        application = service.get_application(
            application_id
        )

        if application is None:
            print("Application not found.")
            return

        print("\nApplication to delete:")
        print(f"Position: {application.position}")
        print(f"Status:   {application.status}")

        confirmation = input(
            "Are you sure you want to delete this "
            "application? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        deleted = service.delete_application(
            application_id
        )

        if deleted:
            print(
                "\nApplication deleted successfully!"
            )
        else:
            print("Application not found.")