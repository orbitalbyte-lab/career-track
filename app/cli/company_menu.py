from app.database.connection import SessionLocal
from app.services.company_service import CompanyService


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

        name = input(f"Name [{company.name}]: ").strip()

        industry = input(f"Industry [{company.industry or 'N/A'}]: ").strip()

        location = input(f"Location [{company.location or 'N/A'}]: ").strip()

        website = input(f"Website [{company.website or 'N/A'}]: ").strip()

        notes = input(f"Notes [{company.notes or 'N/A'}]: ").strip()

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

        confirmation = (
            input("Are you sure you want to delete this company? (y/n): ")
            .strip()
            .lower()
        )

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
