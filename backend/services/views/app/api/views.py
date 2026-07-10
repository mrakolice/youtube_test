from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import requests as req
from app.api import responses as res
from app.db.session import get_db

router = APIRouter(prefix="/api/views", tags=["views"])


@router.post("/record")
async def record_view(
    view_data: req.RecordViewRequest,
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> dict:
    """Record a video view."""
    # TODO: Implement view recording
    return {"message": "View recorded"}


@router.get("/{video_id}/count", response_model=res.ViewCountResponse)
async def get_view_count(
    video_id: int,
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.ViewCountResponse:
    """Get view count for a video."""
    # TODO: Implement view count retrieval
    return res.ViewCountResponse(
        video_id=video_id,
        total_views=0,
        unique_views=0,
    )
