from pydantic import BaseModel


class RecordViewRequest(BaseModel):
    """Request model for recording view."""
    
    video_id: int
    watched_duration: int = 0


class VideoViewCountResponse(BaseModel):
    """Response model for video view count."""
    
    video_id: int
    total_views: int
    unique_views: int
