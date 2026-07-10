from pydantic import BaseModel


class AddReactionRequest(BaseModel):
    """Request model for adding reaction."""
    
    video_id: int
    reaction_type: str  # 'like' or 'dislike'


class ReactionStatsResponse(BaseModel):
    """Response model for reaction stats."""
    
    video_id: int
    likes: int
    dislikes: int
