from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class VideoView(SQLModel, table=True):
    """View tracking model."""

    __tablename__ = "video_views"

    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: int = Field(index=True)
    user_id: Optional[int] = Field(default=None, index=True)
    viewer_ip: str = Field(max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)
    watched_duration: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
