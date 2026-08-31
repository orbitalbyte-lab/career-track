from datetime import datetime, timedelta

import pytest

from app.models.interview import (
    Interview,
    InterviewStatus,
    InterviewType,
)
from app.services.interview_service import (
    InterviewService,
)


def create_interview(
    interview_type=InterviewType.ONLINE,
    status=InterviewStatus.SCHEDULED,
    scheduled_at=None,
):
    return Interview(
        application_id=1,
        scheduled_at=(
            scheduled_at
            or datetime(2026, 9, 1, 10, 0)
        ),
        interview_type=interview_type,
        status=status,
    )


def test_interview_model():
    interview = create_interview()

    assert interview.application_id == 1
    assert (
        interview.interview_type
        == InterviewType.ONLINE
    )
    assert (
        interview.status
        == InterviewStatus.SCHEDULED
    )

def test_interview_rejects_invalid_application_id():
    with pytest.raises(
        ValueError,
        match="Invalid application ID",
    ):
        Interview(
            application_id=0,
            scheduled_at=datetime(2026, 9, 1, 10, 0),
            interview_type=InterviewType.ONLINE,
            status=InterviewStatus.SCHEDULED,
        )


def test_interview_rejects_invalid_interview_type():
    with pytest.raises(
        ValueError,
        match="Invalid interview type",
    ):
        Interview(
            application_id=1,
            scheduled_at=datetime(2026, 9, 1, 10, 0),
            interview_type="Invalid",
            status=InterviewStatus.SCHEDULED,
        )


def test_interview_rejects_invalid_status():
    with pytest.raises(
        ValueError,
        match="Invalid interview status",
    ):
        Interview(
            application_id=1,
            scheduled_at=datetime(2026, 9, 1, 10, 0),
            interview_type=InterviewType.ONLINE,
            status="Invalid",
        )


def test_interview_rejects_invalid_outcome():
    with pytest.raises(
        ValueError,
        match="Invalid interview outcome",
    ):
        Interview(
            application_id=1,
            scheduled_at=datetime(2026, 9, 1, 10, 0),
            interview_type=InterviewType.ONLINE,
            status=InterviewStatus.SCHEDULED,
            outcome="Invalid",
        )    


def test_create_interview(db_session):
    service = InterviewService(db_session)

    interview = create_interview()

    result = service.create_interview(interview)

    assert result.id is not None
    assert result.application_id == 1
    assert result.interview_type == "Online"
    assert result.status == "Scheduled"


def test_get_interviews(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview()
    )
    service.create_interview(
        create_interview(
            interview_type=InterviewType.PHONE
        )
    )

    results = service.get_interviews()

    assert len(results) == 2


def test_get_interview(db_session):
    service = InterviewService(db_session)

    created = service.create_interview(
        create_interview()
    )

    result = service.get_interview(
        created.id
    )

    assert result is not None
    assert result.id == created.id


def test_get_interview_returns_none_for_missing_id(
    db_session,
):
    service = InterviewService(db_session)

    result = service.get_interview(999)

    assert result is None


def test_update_interview(db_session):
    service = InterviewService(db_session)

    created = service.create_interview(
        create_interview()
    )

    result = service.update_interview(
        created.id,
        "Completed",
        "Passed",
    )

    assert result is not None
    assert result.status == "Completed"
    assert result.outcome == "Passed"


def test_update_interview_defaults_outcome_to_pending(
    db_session,
):
    service = InterviewService(db_session)

    created = service.create_interview(
        create_interview()
    )

    result = service.update_interview(
        created.id,
        "Completed",
    )

    assert result is not None
    assert result.status == "Completed"
    assert result.outcome == "Pending"


def test_update_interview_returns_none_for_missing_id(
    db_session,
):
    service = InterviewService(db_session)

    result = service.update_interview(
        999,
        "Completed",
    )

    assert result is None


def test_delete_interview(db_session):
    service = InterviewService(db_session)

    created = service.create_interview(
        create_interview()
    )

    result = service.delete_interview(
        created.id
    )

    assert result is True
    assert service.get_interview(
        created.id
    ) is None


def test_delete_interview_returns_false_for_missing_id(
    db_session,
):
    service = InterviewService(db_session)

    result = service.delete_interview(999)

    assert result is False


def test_get_interview_statistics(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            status=InterviewStatus.SCHEDULED
        )
    )
    service.create_interview(
        create_interview(
            status=InterviewStatus.COMPLETED
        )
    )
    service.create_interview(
        create_interview(
            status=InterviewStatus.COMPLETED
        )
    )

    statistics = (
        service.get_interview_statistics()
    )

    assert statistics == {
        "Scheduled": 1,
        "Completed": 2,
    }


def test_get_upcoming_interviews(db_session):
    service = InterviewService(db_session)

    future_date = datetime.now() + timedelta(days=7)

    service.create_interview(
        create_interview(
            scheduled_at=future_date
        )
    )

    results = (
        service.get_upcoming_interviews()
    )

    assert len(results) >= 1


def test_search_interviews(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview()
    )

    results = service.search_interviews(
        "Scheduled"
    )

    assert len(results) == 1
    assert results[0].status == "Scheduled"


def test_search_interviews_by_type(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            interview_type=InterviewType.PHONE
        )
    )

    results = service.search_interviews(
        "Phone"
    )

    assert len(results) == 1
    assert results[0].interview_type == "Phone"


def test_get_interviews_by_status(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            status=InterviewStatus.SCHEDULED
        )
    )
    service.create_interview(
        create_interview(
            status=InterviewStatus.COMPLETED
        )
    )

    results = service.get_interviews_by_status(
        "Scheduled"
    )

    assert len(results) == 1
    assert results[0].status == "Scheduled"


def test_get_interview_analytics(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            interview_type=InterviewType.ONLINE,
            status=InterviewStatus.COMPLETED,
        )
    )

    service.create_interview(
        create_interview(
            interview_type=InterviewType.PHONE,
            status=InterviewStatus.SCHEDULED,
        )
    )

    analytics = (
        service.get_interview_analytics()
    )

    assert analytics["total"] == 2
    assert analytics["completed"] == 1
    assert analytics["online"] == 1
    assert analytics["phone"] == 1


def test_get_recent_interviews(db_session):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            scheduled_at=datetime(
                2026, 8, 1, 10, 0
            )
        )
    )

    service.create_interview(
        create_interview(
            scheduled_at=datetime(
                2026, 8, 5, 10, 0
            )
        )
    )

    results = (
        service.get_recent_interviews()
    )

    assert len(results) == 2
    assert (
        results[0].scheduled_at
        > results[1].scheduled_at
    )


def test_get_sorted_interviews_by_date(
    db_session,
):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            scheduled_at=datetime(
                2026, 8, 1, 10, 0
            )
        )
    )

    service.create_interview(
        create_interview(
            scheduled_at=datetime(
                2026, 8, 5, 10, 0
            )
        )
    )

    results = service.get_sorted_interviews(
        "date"
    )

    assert (
        results[0].scheduled_at
        > results[1].scheduled_at
    )


def test_get_sorted_interviews_by_type(
    db_session,
):
    service = InterviewService(db_session)

    service.create_interview(
        create_interview(
            interview_type=InterviewType.PHONE
        )
    )

    service.create_interview(
        create_interview(
            interview_type=InterviewType.ONLINE
        )
    )

    results = service.get_sorted_interviews(
        "type"
    )

    assert results[0].interview_type == "Online"
    assert results[1].interview_type == "Phone"


def test_get_this_week_interviews(db_session):
    service = InterviewService(db_session)

    # The repository determines the current week,
    # so use a datetime that is definitely in the
    # current week.
    now = datetime.now()

    service.create_interview(
        create_interview(
            scheduled_at=now + timedelta(hours=1)
        )
    )

    results = (
        service.get_this_week_interviews()
    )

    assert len(results) >= 1