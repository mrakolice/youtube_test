from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, Float
from sqlmodel import Field, SQLModel


class Video(SQLModel, table=True):
    """Video model for video service."""
    
    __tablename__ = "videos"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(Integer),
    )
    user_id: int = Field(
        index=True,
        sa_column=Column(Integer, nullable=False),
    )
    title: str = Field(
        max_length=255,
        sa_column=Column(String(255), nullable=False),
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
    )
    duration: float = Field(
        sa_column=Column(Float, nullable=False),
    )
    thumbnail_url: Optional[str] = Field(
        default=None,
        max_length=500,
        sa_column=Column(String(500)),
    )
    original_file_path: str = Field(
        max_length=500,
        sa_column=Column(String(500), nullable=False),
    )
    is_processed: bool = Field(
        default=False,
        sa_column=Column(Integer, default=0),
    )
    is_published: bool = Field(
        default=False,
        sa_column=Column(Integer, default=0),
    )
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


class VideoQuality(SQLModel, table=True):
    """Video quality variant model."""
    
    __tablename__ = "video_qualities"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(Integer),
    )
    video_id: int = Field(
        index=True,
        sa_column=Column(Integer, nullable=False),
    )
    quality: str = Field(
        index=True,
        max_length=50,
        sa_column=Column(String(50), nullable=False),
    )  # 360p, 480p, 720p, 1080p
    file_path: str = Field(
        max_length=500,
        sa_column=Column(String(500), nullable=False),
    )
    bitrate: str = Field(
        max_length=50,
        sa_column=Column(String(50), nullable=False),
    )  # e.g., "500k", "2500k"
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )

    class Config:
        arbitrary_types_allowed = True
