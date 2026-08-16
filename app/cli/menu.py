from datetime import date
from datetime import datetime

from app.database.connection import SessionLocal

from app.models.application import (
    ApplicationStatus,
    ApplicationType,
)
from app.models.interview import (
    Interview,
    InterviewType,
)

from app.services.application_service import (
    ApplicationService,
)
from app.services.company_service import (
    CompanyService,
)
from app.services.export_service import (
    ExportService,
)
from app.services.import_service import (
    ImportService,
)
from app.services.interview_service import (
    InterviewService,
)

def show_menu() -> None:
    print()
    print("=" * 40)
    print("          CAREERTRACK")
    print("=" * 40)
    print("1. Add company")
    print("2. List companies")
    print("3. View company")
    print("4. Update company")
    print("5. Delete company")
    print("6. Search companies")
    print("7. Add application")
    print("8. List applications")
    print("9. View application")
    print("10. Update application")
    print("11. Delete application")
    print("12. Search applications")
    print("13. Dashboard")
    print("14. Filter applications")
    print("15. Export applications to CSV")
    print("16. Sort applications")
    print("17. Import applications from CSV")
    print("18. Add interview")
    print("19. List interviews")
    print("20. Exit")
def add_company() -> None:
    print("\n--- Add Company ---")

    name = input("Company name: ").strip()
    industry = input("Industry (optional): ").strip() or None
    location = input("Location (optional): ").strip() or None
    website = input("Website (optional): ").strip() or None

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.create_company(
            name=name,
            industry=industry,
            location=location,
            website=website,
        )

        print("\nCompany created successfully!")
        print(f"Company ID: {company.id}")


def list_companies() -> None:
    print("\n--- Companies ---")

    with SessionLocal() as session:
        service = CompanyService(session)

        companies = service.get_companies()

        if not companies:
            print("No companies found.")
            return

        for company in companies:
            print(
                f"[{company.id}] "
                f"{company.name} | "
                f"{company.industry or 'N/A'} | "
                f"{company.location or 'N/A'}"
            )


def search_companies() -> None:
    print("\n--- Search Companies ---")

    query = input("Search company name: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    with SessionLocal() as session:
        service = CompanyService(session)

        companies = service.search_companies(query)

        if not companies:
            print("No companies found.")
            return

        print(f"\nSearch results for: {query}")
        print("-" * 60)

        for company in companies:
            print(
                f"[{company.id}] "
                f"{company.name} | "
                f"{company.industry or 'N/A'} | "
                f"{company.location or 'N/A'}"
            )

        print("-" * 60)


def view_company() -> None:
    print("\n--- View Company ---")

    try:
        company_id = int(input("Company ID: ").strip())
    except ValueError:
        print("Company ID must be a number.")
        return

    with SessionLocal() as session:
        service = CompanyService(session)
        company = service.get_company(company_id)

        if company is None:
            print("Company not found.")
            return

        print("\nCompany Details")
        print("-" * 30)
        print(f"ID:       {company.id}")
        print(f"Name:     {company.name}")
        print(f"Industry: {company.industry or 'N/A'}")
        print(f"Location: {company.location or 'N/A'}")
        print(f"Website:  {company.website or 'N/A'}")
        print(f"Notes:    {company.notes or 'N/A'}")
        print("-" * 30)


def update_company() -> None:
    print("\n--- Update Company ---")

    try:
        company_id = int(input("Company ID: ").strip())
    except ValueError:
        print("Company ID must be a number.")
        return

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.get_company(company_id)

        if company is None:
            print("Company not found.")
            return

        print("\nPress Enter to keep the current value.")

        name = input(
            f"Name [{company.name}]: "
        ).strip()

        industry = input(
            f"Industry [{company.industry or 'N/A'}]: "
        ).strip()

        location = input(
            f"Location [{company.location or 'N/A'}]: "
        ).strip()

        website = input(
            f"Website [{company.website or 'N/A'}]: "
        ).strip()

        notes = input(
            f"Notes [{company.notes or 'N/A'}]: "
        ).strip()

        try:
            updated_company = service.update_company(
                company_id=company_id,
                name=name if name else None,
                industry=industry if industry else None,
                location=location if location else None,
                website=website if website else None,
                notes=notes if notes else None,
            )

            if updated_company is None:
                print("Company not found.")
                return

            print("\nCompany updated successfully!")

        except ValueError as error:
            print(f"\nError: {error}")


def delete_company() -> None:
    print("\n--- Delete Company ---")

    try:
        company_id = int(input("Company ID: ").strip())
    except ValueError:
        print("Company ID must be a number.")
        return

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.get_company(company_id)

        if company is None:
            print("Company not found.")
            return

        print("\nCompany to delete:")
        print(f"Name:     {company.name}")
        print(f"Industry: {company.industry or 'N/A'}")
        print(f"Location: {company.location or 'N/A'}")

        confirmation = input(
            "Are you sure you want to delete this company? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        try:
            deleted = service.delete_company(company_id)

            if deleted:
                print("\nCompany deleted successfully!")
            else:
                print("Company not found.")

        except ValueError as error:
            print(f"\nError: {error}")


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

    application_type_choice = input(
        "Application type: "
    ).strip()

    try:
        application_type_index = (
            int(application_type_choice) - 1
        )

        application_type = application_types[
            application_type_index
        ].value

    except (ValueError, IndexError):
        print("Invalid application type selection.")
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
        print(f"{index}. {application_status.value}")

    status_choice = input("Status: ").strip()

    try:
        status_index = int(status_choice) - 1
        status = statuses[status_index].value

    except (ValueError, IndexError):
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
                application_type=application_type,
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
    print("\n--- Applications (Newest First) ---")

    with SessionLocal() as session:
        service = ApplicationService(session)

        applications = (
            service.get_recent_applications()
        )

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
def show_dashboard() -> None:
    print("\n--- CareerTrack Dashboard ---")

    with SessionLocal() as session:
        service = ApplicationService(session)

        statistics = service.get_dashboard_statistics()

        monthly_applications = (
            service.get_monthly_application_counts()
        )
        location_statistics = (
            service.get_location_statistics()
        )

        total = statistics["total"]
        total_companies = statistics["total_companies"]
        success_rate = statistics["success_rate"]
        by_status = statistics["by_status"]
        by_application_type = statistics[
            "by_application_type"
        ]
        by_company = statistics["by_company"]

        # Get recent applications and upcoming deadlines
        recent_applications = service.get_recent_applications()

        upcoming_deadlines = service.get_upcoming_deadlines(
            today=date.today(),
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
            for status, count in sorted(
                by_status.items()
            ):
                print(f"{status}: {count}")
        else:
            print("No applications found.")

        print("\nApplications by Type")
        print("-" * 35)

        if by_application_type:
            for application_type, count in sorted(
                by_application_type.items()
            ):
                print(f"{application_type}: {count}")
        else:
            print("No applications found.")

        print("\nApplications by Company")
        print("-" * 35)

        if by_company:
            for company, count in sorted(
                by_company.items()
            ):
                print(f"{company}: {count}")
        else:
            print("No applications found.")

        print("\nApplications by Month")
        print("-" * 35)

        if monthly_applications:
            for month, count in sorted(
                monthly_applications.items()
            ):
                print(f"{month}: {count}")
        else:
            print("No applications found.")

        print("-" * 35)

        print("\nApplications by Location")
        print("-" * 35)

        if location_statistics:
            for location, count in sorted(
                location_statistics.items()
            ):
                print(f"{location}: {count}")
        else:
            print("No applications found.")

        print("-" * 35)

        print("\nRecent Applications")
        print("-" * 35)

        if recent_applications:
            for application in recent_applications:
                company_name = (
                    application.company.name
                    if application.company
                    else "N/A"
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
                    application.company.name
                    if application.company
                    else "N/A"
                )

                print(
                    f"{application.position} | "
                    f"{company_name} | "
                    f"Deadline: {application.deadline} | "
                    f"Status: {application.status}"
                )
        else:
            print("No upcoming deadlines.")

        print("-" * 60)
def export_applications() -> None:
    print("\n--- Export Applications ---")

    with SessionLocal() as session:
        application_service = (
            ApplicationService(session)
        )

        exporter = ExportService(
            application_service
        )

        path = (
            exporter.export_applications_to_csv()
        )

        print(
            f"Applications exported to: {path}"
        )
def import_applications() -> None:
    print("\n--- Import Applications ---")

    file_path = input(
        "CSV file path: "
    ).strip()

    with SessionLocal() as session:
        application_service = (
            ApplicationService(session)
        )

        importer = ImportService(
            application_service
        )

        try:
            rows = (
                importer.import_applications_from_csv(
                    file_path
                )
            )

            print(
                f"Imported {len(rows)} applications."
            )

        except FileNotFoundError as error:
            print(error)  
def add_interview() -> None:
    print("\n--- Add Interview ---")

    application_id = int(
        input("Application ID: ").strip()
    )

    scheduled_at = datetime.fromisoformat(
        input(
            "Interview date and time (YYYY-MM-DD HH:MM): "
        )
    )

    interview_type = InterviewType(
        input(
            "Interview type (Online/Phone/On-site): "
        ).strip()
    )

    notes = (
        input("Notes (optional): ").strip()
        or None
    )

    interview = Interview(
        application_id=application_id,
        scheduled_at=scheduled_at,
        interview_type=interview_type,
        notes=notes,
    )

    with SessionLocal() as session:
        interview_service = (
            InterviewService(session)
        )

        interview_service.create_interview(
            interview
        )

    print("Interview scheduled successfully.")


def list_interviews() -> None:
    print("\n--- Interviews ---")

    with SessionLocal() as session:
        interview_service = (
            InterviewService(session)
        )

        interviews = (
            interview_service.get_interviews()
        )

        if not interviews:
            print("No interviews found.")
            return

        for interview in interviews:
            print(
                f"Application ID: "
                f"{interview.application_id} | "
                f"{interview.interview_type} | "
                f"{interview.scheduled_at}"
            )                  
def run() -> None:
    while True:
        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            add_company()

        elif choice == "2":
            list_companies()

        elif choice == "3":
            view_company()

        elif choice == "4":
            update_company()

        elif choice == "5":
            delete_company()

        elif choice == "6":
            search_companies()

        elif choice == "7":
            add_application()

        elif choice == "8":
            list_applications()

        elif choice == "9":
            view_application()

        elif choice == "10":
            update_application()

        elif choice == "11":
            delete_application()

        elif choice == "12":
            search_applications()

        elif choice == "13":
            show_dashboard()

        elif choice == "14":
            filter_applications()

        elif choice == "15":
            export_applications()

        elif choice == "16":
            sort_applications()

        elif choice == "17":
            import_applications()

        elif choice == "18":
            add_interview()

        elif choice == "19":
            list_interviews()

        elif choice == "20":
            print("\nGoodbye!")
            break

        else:
            print(
                "\nInvalid choice. Please choose 1-20."
            )