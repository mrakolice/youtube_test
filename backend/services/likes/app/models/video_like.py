from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class VideoLike(SQLModel, table=True):
    """Like/Dislike model."""

    __tablename__ = "video_likes"

    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: int = Field(index=True)
    user_id: int = Field(index=True)
    reaction_type: str = Field(index=True, max_length=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
