from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    """Naive UTC timestamp: datetime.utcnow() is deprecated from Python 3.12 on,
    and the created_at/updated_at columns are DateTime() without a timezone."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class VideoLike(SQLModel, table=True):
    """Like/Dislike model."""

    __tablename__ = "video_likes"

    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: int = Field(index=True)
    user_id: int = Field(index=True)
    reaction_type: str = Field(index=True, max_length=10)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Config:
        arbitrary_types_allowed = True
