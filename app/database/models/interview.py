from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.models.application import (
    ApplicationDB,
)
from app.database.utc_datetime import UTCDateTime


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

    scheduled_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
    )
    interview_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
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

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    application: Mapped[ApplicationDB] = relationship()
