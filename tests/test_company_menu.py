from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.cli import company_menu


def make_company(
    company_id=1,
    name="Microsoft",
    industry="Technology",
    location="Seattle",
    website="https://microsoft.com",
    notes="Software company",
):
    return SimpleNamespace(
        id=company_id,
        name=name,
        industry=industry,
        location=location,
        website=website,
        notes=notes,
        applications=[],
    )


def test_add_company():
    company = make_company()

    session = MagicMock()
    service = MagicMock()
    service.create_company.return_value = company

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "Microsoft",
            "Technology",
            "Seattle",
            "https://microsoft.com",
        ],
    ):
        company_menu.add_company()

    service.create_company.assert_called_once_with(
        name="Microsoft",
        industry="Technology",
        location="Seattle",
        website="https://microsoft.com",
    )


def test_list_companies(capsys):
    companies = [
        make_company(
            company_id=1,
            name="Microsoft",
            industry="Technology",
            location="Seattle",
        ),
        make_company(
            company_id=2,
            name="Google",
            industry="Technology",
            location="Mountain View",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_companies.return_value = companies

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ):
        company_menu.list_companies()

    output = capsys.readouterr().out

    assert "Microsoft" in output
    assert "Google" in output
    assert "Seattle" in output
    assert "Mountain View" in output


def test_list_companies_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_companies.return_value = []

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ):
        company_menu.list_companies()

    output = capsys.readouterr().out

    assert "No companies found." in output


def test_search_companies_rejects_empty_query(capsys):
    with patch(
        "builtins.input",
        return_value="   ",
    ):
        company_menu.search_companies()

    output = capsys.readouterr().out

    assert "Search query cannot be empty." in output


def test_search_companies(capsys):
    companies = [
        make_company(name="Microsoft"),
        make_company(
            company_id=2,
            name="Microsoft Research",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.search_companies.return_value = companies

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="Microsoft",
    ):
        company_menu.search_companies()

    output = capsys.readouterr().out

    assert "Search results for: Microsoft" in output
    assert "Microsoft" in output
    assert "Microsoft Research" in output


def test_search_companies_when_no_results(capsys):
    session = MagicMock()
    service = MagicMock()
    service.search_companies.return_value = []

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="Unknown",
    ):
        company_menu.search_companies()

    output = capsys.readouterr().out

    assert "No companies found." in output


def test_view_company_with_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        company_menu.view_company()

    output = capsys.readouterr().out

    assert "Company ID must be a number." in output


def test_view_company_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = None

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="999",
    ):
        company_menu.view_company()

    output = capsys.readouterr().out

    assert "Company not found." in output


def test_view_company(capsys):
    company = make_company()

    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = company

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="1",
    ):
        company_menu.view_company()

    output = capsys.readouterr().out

    assert "Company Details" in output
    assert "Microsoft" in output
    assert "Technology" in output
    assert "Seattle" in output
    assert "https://microsoft.com" in output
    assert "Software company" in output


def test_update_company_with_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        company_menu.update_company()

    output = capsys.readouterr().out

    assert "Company ID must be a number." in output


def test_update_company_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = None

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="999",
    ):
        company_menu.update_company()

    output = capsys.readouterr().out

    assert "Company not found." in output


def test_update_company(capsys):
    company = make_company()

    updated_company = make_company(
        name="Google",
        industry="Technology",
        location="California",
        website="https://google.com",
        notes="Updated notes",
    )

    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = company
    service.update_company.return_value = updated_company

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "1",
            "Google",
            "Technology",
            "California",
            "https://google.com",
            "Updated notes",
        ],
    ):
        company_menu.update_company()

    service.update_company.assert_called_once_with(
        company_id=1,
        name="Google",
        industry="Technology",
        location="California",
        website="https://google.com",
        notes="Updated notes",
    )

    output = capsys.readouterr().out

    assert "Company updated successfully!" in output


def test_update_company_handles_value_error(capsys):
    company = make_company()

    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = company
    service.update_company.side_effect = ValueError(
        "Company name cannot be empty."
    )

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "1",
            "",
            "Technology",
            "Seattle",
            "https://microsoft.com",
            "Notes",
        ],
    ):
        company_menu.update_company()

    output = capsys.readouterr().out

    assert "Error: Company name cannot be empty." in output


def test_delete_company_with_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        company_menu.delete_company()

    output = capsys.readouterr().out

    assert "Company ID must be a number." in output


def test_delete_company_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = None

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="999",
    ):
        company_menu.delete_company()

    output = capsys.readouterr().out

    assert "Company not found." in output


def test_delete_company_cancelled(capsys):
    company = make_company()

    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = company

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=["1", "n"],
    ):
        company_menu.delete_company()

    service.delete_company.assert_not_called()

    output = capsys.readouterr().out

    assert "Deletion cancelled." in output


def test_delete_company(capsys):
    company = make_company()

    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = company
    service.delete_company.return_value = True

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=["1", "y"],
    ):
        company_menu.delete_company()

    service.delete_company.assert_called_once_with(1)

    output = capsys.readouterr().out

    assert "Company deleted successfully!" in output


def test_delete_company_handles_value_error(capsys):
    company = make_company()

    session = MagicMock()
    service = MagicMock()
    service.get_company.return_value = company
    service.delete_company.side_effect = ValueError(
        "Cannot delete company with 2 application(s)."
    )

    with patch.object(
        company_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        company_menu,
        "CompanyService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=["1", "y"],
    ):
        company_menu.delete_company()

    output = capsys.readouterr().out

    assert (
        "Cannot delete company with 2 application(s)."
        in output
    )