"""create bookings table"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_bookings"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("booking_date", sa.Date(), nullable=False),
        sa.Column("booking_time", sa.Time(), nullable=False),
        sa.Column("guests", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
    )
    op.create_index("ix_bookings_booking_date", "bookings", ["booking_date"])
    op.create_index("ix_bookings_booking_time", "bookings", ["booking_time"])


def downgrade() -> None:
    op.drop_index("ix_bookings_booking_time", table_name="bookings")
    op.drop_index("ix_bookings_booking_date", table_name="bookings")
    op.drop_table("bookings")
