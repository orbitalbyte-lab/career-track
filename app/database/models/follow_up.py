from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.connection import Base
from app.database.models.application import (
    ApplicationDB,
)


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
        DateTime,
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