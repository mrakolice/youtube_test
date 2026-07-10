from pydantic import BaseModel
from datetime import datetime


class ViewResponse(BaseModel):
    """Response model for view."""
    
    id: int
    video_id: int
    watched_duration: int
    created_at: datetime


class ViewCountResponse(BaseModel):
    """Response model for view count."""
    
    video_id: int
    total_views: int
    unique_views: int
