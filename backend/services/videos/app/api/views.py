from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import requests as req
from app.api import responses as res
from app.db.session import get_db

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.post("/upload", response_model=res.VideoUploadResponse)
async def upload_video(
    video_upload: req.VideoUploadRequest,
    file: UploadFile = File(...),
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.VideoUploadResponse:
    """Upload a new video."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )
    
    # TODO: Implement video upload and processing
    return res.VideoUploadResponse(
        id=1,
        message="Video uploaded successfully",
        upload_status="processing",
    )


@router.get("/{video_id}", response_model=res.VideoWithQualitiesResponse)
async def get_video(
    video_id: int,
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.VideoWithQualitiesResponse:
    """Get video details."""
    # TODO: Implement video retrieval
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Video not found",
    )


@router.get("/", response_model=list[res.VideoResponse])
async def list_videos(
    skip: int = 0,
    limit: int = 10,
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> list[res.VideoResponse]:
    """List videos."""
    # TODO: Implement video listing
    return []
