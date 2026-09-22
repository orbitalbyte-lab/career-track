from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.database.models.application import ApplicationDB
    from app.database.models.user import UserDB

class CompanyDB(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    user: Mapped["UserDB | None"] = relationship(
        back_populates="companies",
    )

    applications: Mapped[list["ApplicationDB"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )
