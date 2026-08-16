from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base
from app.models.interview import (
    Interview,
    InterviewStatus,
    InterviewType,
)
from app.repositories.interview_repository import (
    InterviewRepository,
)


def test_create_interview():
    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    with Session() as session:
        repository = InterviewRepository(
            session
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
            interview_type=(
                InterviewType.ONLINE
            ),
            status=(
                InterviewStatus.SCHEDULED
            ),
        )

        result = repository.create(
            interview
        )

        assert result.id == 1


def test_get_all_interviews():
    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    with Session() as session:
        repository = InterviewRepository(
            session
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
            interview_type=(
                InterviewType.ONLINE
            ),
            status=(
                InterviewStatus.SCHEDULED
            ),
        )

        repository.create(interview)

        interviews = (
            repository.get_all()
        )

        assert len(interviews) == 1


def test_delete_interview():
    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    with Session() as session:
        repository = InterviewRepository(
            session
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
            interview_type=(
                InterviewType.ONLINE
            ),
            status=(
                InterviewStatus.SCHEDULED
            ),
        )

        created = repository.create(
            interview
        )

        result = repository.delete(
            created.id
        )

        assert result is True

        assert (
            repository.get_by_id(
                created.id
            )
            is None
        )       