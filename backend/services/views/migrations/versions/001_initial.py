"""Initial migration - create video views table

Revision ID: 001_initial
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "video_views",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("video_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("viewer_ip", sa.String(45), nullable=False),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("watched_duration", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_video_views_video_id"), "video_views", ["video_id"])
    op.create_index(op.f("ix_video_views_user_id"), "video_views", ["user_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_video_views_user_id"), table_name="video_views")
    op.drop_index(op.f("ix_video_views_video_id"), table_name="video_views")
    op.drop_table("video_views")
