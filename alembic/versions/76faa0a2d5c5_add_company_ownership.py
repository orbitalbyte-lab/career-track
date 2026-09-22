"""add company ownership

Revision ID: 76faa0a2d5c5
Revises: 209bd14ad33b
Create Date: 2026-09-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = "76faa0a2d5c5"
down_revision: Union[str, Sequence[str], None] = "209bd14ad33b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add company ownership fields."""
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("companies")
    }

    if "user_id" not in columns:
        op.add_column(
            "companies",
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True,
            ),
        )

    indexes = {
        index["name"]
        for index in inspector.get_indexes("companies")
    }

    if "ix_companies_user_id" not in indexes:
        op.create_index(
            "ix_companies_user_id",
            "companies",
            ["user_id"],
            unique=False,
        )

    foreign_keys = inspector.get_foreign_keys("companies")

    has_user_foreign_key = any(
        foreign_key.get("name") == "companies_user_id_fkey"
        and foreign_key.get("referred_table") == "users"
        and foreign_key.get("constrained_columns") == ["user_id"]
        and foreign_key.get("referred_columns") == ["id"]
        for foreign_key in foreign_keys
    )

    if not has_user_foreign_key:
        op.create_foreign_key(
            "companies_user_id_fkey",
            "companies",
            "users",
            ["user_id"],
            ["id"],
        )


def downgrade() -> None:
    """Remove company ownership fields."""
    bind = op.get_bind()
    inspector = inspect(bind)

    foreign_keys = inspector.get_foreign_keys("companies")

    for foreign_key in foreign_keys:
        if foreign_key.get("name") == "companies_user_id_fkey":
            op.drop_constraint(
                "companies_user_id_fkey",
                "companies",
                type_="foreignkey",
            )
            break

    indexes = {
        index["name"]
        for index in inspector.get_indexes("companies")
    }

    if "ix_companies_user_id" in indexes:
        op.drop_index(
            "ix_companies_user_id",
            table_name="companies",
        )

    columns = {
        column["name"]
        for column in inspector.get_columns("companies")
    }

    if "user_id" in columns:
        op.drop_column("companies", "user_id")