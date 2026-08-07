"""add soft delete support

Revision ID: e43725af23ba
Revises: b1dafea1031f
Create Date: 2026-08-06 15:40:27.210079

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e43725af23ba"
down_revision: Union[str, Sequence[str], None] = "b1dafea1031f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Applications
    op.add_column(
        "applications",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.alter_column("applications", "is_deleted", server_default=None)

    op.add_column(
        "applications",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Companies
    op.add_column(
        "companies",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.alter_column("companies", "is_deleted", server_default=None)

    op.add_column(
        "companies",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Opportunities
    op.add_column(
        "opportunities",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.alter_column("opportunities", "is_deleted", server_default=None)

    op.add_column(
        "opportunities",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Student Profile
    op.add_column(
        "student_profile",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.alter_column("student_profile", "is_deleted", server_default=None)

    op.add_column(
        "student_profile",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("student_profile", "deleted_at")
    op.drop_column("student_profile", "is_deleted")

    op.drop_column("opportunities", "deleted_at")
    op.drop_column("opportunities", "is_deleted")

    op.drop_column("companies", "deleted_at")
    op.drop_column("companies", "is_deleted")

    op.drop_column("applications", "deleted_at")
    op.drop_column("applications", "is_deleted")