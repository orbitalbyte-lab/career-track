from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class CompanyDB(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    applications: Mapped[list["ApplicationDB"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )