from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.models.application import (
    ApplicationDB,
)
from app.database.utc_datetime import UTCDateTime


class FollowUpDB(Base):
    __tablename__ = "follow_ups"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False,
    )

    follow_up_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
    )
    note: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    application: Mapped[ApplicationDB] = relationship()
