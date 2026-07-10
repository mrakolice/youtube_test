from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field, SQLModel


class VideoLike(SQLModel, table=True):
    """Like/Dislike model."""
    
    __tablename__ = "video_likes"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(Integer),
    )
    video_id: int = Field(
        index=True,
        sa_column=Column(Integer, nullable=False),
    )
    user_id: int = Field(
        index=True,
        sa_column=Column(Integer, nullable=False),
    )
    reaction_type: str = Field(
        index=True,
        max_length=10,
        sa_column=Column(String(10), nullable=False),
    )  # 'like' or 'dislike'
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )

    class Config:
        arbitrary_types_allowed = True
