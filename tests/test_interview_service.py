from datetime import datetime

from app.models.interview import (
    Interview,
    InterviewStatus,
    InterviewType,
)
from app.services.interview_service import (
    InterviewService,
)


def test_interview_model():
    interview = Interview(
        application_id=1,
        scheduled_at=datetime(
            2026,
            9,
            1,
            10,
            0,
        ),
        interview_type=InterviewType.ONLINE,
        status=InterviewStatus.SCHEDULED,
    )

    assert interview.application_id == 1

    assert (
        interview.interview_type
        == InterviewType.ONLINE
    )

    assert (
        interview.status
        == InterviewStatus.SCHEDULED
    )


def test_search_interviews(db_session):
    service = InterviewService(
        db_session
    )

    interview = Interview(
        application_id=1,
        scheduled_at=datetime(
            2026,
            9,
            1,
            10,
            0,
        ),
        interview_type=InterviewType.ONLINE,
        status=InterviewStatus.SCHEDULED,
    )

    service.create_interview(
        interview
    )

    results = service.search_interviews(
        "Scheduled"
    )

    assert len(results) == 1
    assert results[0].status == "Scheduled"