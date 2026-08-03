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
    print("4. Add application")
    print("5. List applications")
    print("6. Exit")
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
            add_application()
        elif choice == "5":
            list_applications()
        elif choice == "6":
            print("\nGoodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please choose 1-6.")