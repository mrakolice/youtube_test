from pydantic import BaseModel


class LikeResponse(BaseModel):
    """Response model for like."""
    
    video_id: int
    likes_count: int
    dislikes_count: int
    user_reaction: str = None
