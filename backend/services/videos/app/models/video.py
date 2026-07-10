from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Video(SQLModel, table=True):
    """Video model for video service."""

    __tablename__ = "videos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    duration: float = Field()
    thumbnail_url: Optional[str] = Field(default=None, max_length=500)
    original_file_path: str = Field(max_length=500)
    is_processed: bool = Field(default=False)
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True


class VideoQuality(SQLModel, table=True):
    """Video quality variant model."""

    __tablename__ = "video_qualities"

    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: int = Field(index=True)
    quality: str = Field(index=True, max_length=50)
    file_path: str = Field(max_length=500)
    bitrate: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
