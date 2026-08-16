from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    """Naive UTC timestamp: datetime.utcnow() is deprecated from Python 3.12 on,
    and the created_at column is DateTime() without a timezone."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class VideoView(SQLModel, table=True):
    """View tracking model."""

    __tablename__ = "video_views"

    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: int = Field(index=True)
    user_id: Optional[int] = Field(default=None, index=True)
    viewer_ip: str = Field(max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)
    watched_duration: int = Field(default=0)
    created_at: datetime = Field(default_factory=_utcnow)

    class Config:
        arbitrary_types_allowed = True
