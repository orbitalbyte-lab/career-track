from datetime import datetime

from app.models.interview import (
    Interview,
    InterviewStatus,
    InterviewType,
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