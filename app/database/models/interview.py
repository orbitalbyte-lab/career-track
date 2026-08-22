from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.connection import Base
from app.database.models.application import (
    ApplicationDB,
)


class InterviewDB(Base):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False,
    )

    scheduled_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            nullable=False,
        )
    )

    interview_type: Mapped[str] = (
        mapped_column(
            String(50),
            nullable=False,
        )
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    outcome: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Pending",
    )

    notes: Mapped[str | None] = (
        mapped_column(
            String(2000),
            nullable=True,
        )
    )

    application: Mapped[ApplicationDB] = (
        relationship()
    )