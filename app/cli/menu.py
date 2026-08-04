from datetime import date

from app.database.connection import SessionLocal
from app.models.application import ApplicationStatus, ApplicationType
from app.services.application_service import ApplicationService
from app.services.company_service import CompanyService


def show_menu() -> None:
    print()
    print("=" * 40)
    print("          CAREERTRACK")
    print("=" * 40)
    print("1. Add company")
    print("2. List companies")
    print("3. View company")
    print("4. Update company")
    print("5. Add application")
    print("6. List applications")
    print("7. View application")
    print("8. Update application")
    print("9. Delete application")
    print("10. Exit")
    print("=" * 40)


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
        application_types, start=1
    ):
        print(f"{index}. {application_type_option.value}")

    application_type_choice = input("Application type: ").strip()

    try:
        application_type_index = int(application_type_choice) - 1
        application_type = application_types[
            application_type_index
        ].value
    except (ValueError, IndexError):
        print("Invalid application type selection.")
        return

    date_applied = input("Date applied (YYYY-MM-DD): ").strip()

    print("\nSelect application status:")

    statuses = list(ApplicationStatus)

    for index, application_status in enumerate(statuses, start=1):
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

        confirmation = input(
            "Are you sure you want to delete this application? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        deleted = service.delete_application(application_id)

        if deleted:
            print("\nApplication deleted successfully!")
        else:
            print("Application not found.")


def run() -> None:
    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_company()
        elif choice == "2":
            list_companies()
        elif choice == "3":
            view_company()
        elif choice == "4":
            update_company()
        elif choice == "5":
            add_application()
        elif choice == "6":
            list_applications()
        elif choice == "7":
            view_application()
        elif choice == "8":
            update_application()
        elif choice == "9":
            delete_application()
        elif choice == "10":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please choose 1-10.")
