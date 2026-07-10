from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import requests as req
from app.api import responses as res
from app.db.session import get_db

router = APIRouter(prefix="/api/likes", tags=["likes"])


@router.post("/add-reaction")
async def add_reaction(
    reaction_data: req.AddReactionRequest,
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> dict:
    """Add a like or dislike to a video."""
    # TODO: Implement reaction adding
    return {"message": "Reaction recorded"}


@router.get("/{video_id}/stats", response_model=res.LikeResponse)
async def get_like_stats(
    video_id: int,
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.LikeResponse:
    """Get like/dislike stats for a video."""
    # TODO: Implement stats retrieval
    return res.LikeResponse(
        video_id=video_id,
        likes_count=0,
        dislikes_count=0,
    )
