from app.services.application_service import (
    ApplicationService,
)
from app.services.import_service import (
    ImportService,
)


def test_import_applications_from_csv():
    service = ImportService(ApplicationService(None))

    rows = service.import_applications_from_csv("tests/data/sample.csv")

    assert len(rows) == 1

    assert rows[0]["Company"] == "Microsoft"

    assert rows[0]["Position"] == "Software Engineer"
