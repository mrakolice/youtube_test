from pydantic import BaseModel, Field
from typing import Optional


class VideoUploadRequest(BaseModel):
    """Request model for video upload."""
    
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)


class VideoUpdateRequest(BaseModel):
    """Request model for video update."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    is_published: Optional[bool] = None


class VideoPublishRequest(BaseModel):
    """Request model for publishing video."""
    
    is_published: bool = Field(...)
