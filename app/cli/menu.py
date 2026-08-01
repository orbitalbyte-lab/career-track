from app.database.connection import SessionLocal
from app.services.application_service import ApplicationService
from app.services.company_service import CompanyService


def show_menu() -> None:
    print()
    print("=" * 40)
    print("          CAREERTRACK")
    print("=" * 40)
    print("1. Add company")
    print("2. List companies")
    print("3. Add application")
    print("4. List applications")
    print("5. Exit")
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

        print(f"\nCompany created successfully!")
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


def add_application() -> None:
    print("\n--- Add Application ---")

    try:
        company_id = int(input("Company ID: ").strip())
    except ValueError:
        print("Company ID must be a number.")
        return

    position = input("Position: ").strip()
    application_type = input("Application type: ").strip()
    date_applied = input("Date applied (YYYY-MM-DD): ").strip()
    status = input("Status: ").strip()

    from datetime import date

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
                f"{application.status}"
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
            add_application()
        elif choice == "4":
            list_applications()
        elif choice == "5":
            print("\nGoodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please choose 1-5.")