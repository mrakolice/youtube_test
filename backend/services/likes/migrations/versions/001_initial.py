"""Initial migration - create video likes table

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
        "video_likes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("video_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("reaction_type", sa.String(10), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("video_id", "user_id", name="uq_video_user_reaction"),
    )
    op.create_index(op.f("ix_video_likes_video_id"), "video_likes", ["video_id"])
    op.create_index(op.f("ix_video_likes_user_id"), "video_likes", ["user_id"])
    op.create_index(op.f("ix_video_likes_reaction_type"), "video_likes", ["reaction_type"])


def downgrade() -> None:
    op.drop_index(op.f("ix_video_likes_reaction_type"), table_name="video_likes")
    op.drop_index(op.f("ix_video_likes_user_id"), table_name="video_likes")
    op.drop_index(op.f("ix_video_likes_video_id"), table_name="video_likes")
    op.drop_table("video_likes")
