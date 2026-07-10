from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class VideoQualityResponse(BaseModel):
    """Response model for video quality."""
    
    id: int
    quality: str
    bitrate: str


class VideoResponse(BaseModel):
    """Response model for video."""
    
    id: int
    user_id: int
    title: str
    description: Optional[str]
    duration: float
    thumbnail_url: Optional[str]
    is_processed: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime


class VideoWithQualitiesResponse(VideoResponse):
    """Response model for video with qualities."""
    
    qualities: List[VideoQualityResponse] = []


class VideoUploadResponse(BaseModel):
    """Response model for video upload."""
    
    id: int
    message: str
    upload_status: str
