from typing import TYPE_CHECKING
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
if TYPE_CHECKING:
    from app.database.models.company import CompanyDB


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
    )

    companies: Mapped[list["CompanyDB"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )