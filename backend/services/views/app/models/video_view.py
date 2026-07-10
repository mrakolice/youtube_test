from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field, SQLModel


class VideoView(SQLModel, table=True):
    """View tracking model."""
    
    __tablename__ = "video_views"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(Integer),
    )
    video_id: int = Field(
        index=True,
        sa_column=Column(Integer, nullable=False),
    )
    user_id: Optional[int] = Field(
        default=None,
        index=True,
        sa_column=Column(Integer),
    )
    viewer_ip: str = Field(
        max_length=45,
        sa_column=Column(String(45), nullable=False),
    )
    user_agent: Optional[str] = Field(
        default=None,
        max_length=500,
        sa_column=Column(String(500)),
    )
    watched_duration: int = Field(
        sa_column=Column(Integer, nullable=False, server_default="0"),
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )

    class Config:
        arbitrary_types_allowed = True
