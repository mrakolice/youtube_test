"""Initial migration - create videos table

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
        "videos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration", sa.Float(), nullable=False),
        sa.Column("thumbnail_url", sa.String(500), nullable=True),
        sa.Column("original_file_path", sa.String(500), nullable=False),
        sa.Column("is_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_published", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_videos_user_id"), "videos", ["user_id"])
    
    op.create_table(
        "video_qualities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("video_id", sa.Integer(), nullable=False),
        sa.Column("quality", sa.String(50), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("bitrate", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_video_qualities_video_id"), "video_qualities", ["video_id"])
    op.create_index(op.f("ix_video_qualities_quality"), "video_qualities", ["quality"])


def downgrade() -> None:
    op.drop_index(op.f("ix_video_qualities_quality"), table_name="video_qualities")
    op.drop_index(op.f("ix_video_qualities_video_id"), table_name="video_qualities")
    op.drop_table("video_qualities")
    op.drop_index(op.f("ix_videos_user_id"), table_name="videos")
    op.drop_table("videos")
