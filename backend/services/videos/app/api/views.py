import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api import requests as req
from app.api import responses as res
from app.core import config, security
from app.db.session import async_session, get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/videos", tags=["videos"])

ALLOWED_CONTENT_TYPES = {"video/mp4", "video/quicktime", "video/webm", "video/x-matroska"}
UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1 MB


def _video_upload_form(
    title: str = Form(..., min_length=1, max_length=255),
    description: Optional[str] = Form(None, max_length=5000),
) -> req.VideoUploadRequest:
    """Build the upload payload from multipart form fields.

    A plain pydantic model can't be mixed with ``File(...)`` in the same
    request (FastAPI needs either a full JSON body or full multipart form,
    not both), so the request fields are declared as ``Form`` here instead.
    """
    return req.VideoUploadRequest(title=title, description=description)


async def _save_upload_file(file: UploadFile, destination: Path) -> None:
    """Stream the uploaded file to disk, enforcing the configured size limit."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    total_size = 0
    async with aiofiles.open(destination, "wb") as out_file:
        while chunk := await file.read(UPLOAD_CHUNK_SIZE):
            total_size += len(chunk)
            if total_size > config.settings.max_upload_size:
                await out_file.close()
                destination.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File exceeds the maximum allowed upload size",
                )
            await out_file.write(chunk)


async def _extract_duration(file_path: str) -> float:
    """Extract the video duration (in seconds) without blocking the event loop."""

    def _read_duration() -> float:
        from moviepy.editor import VideoFileClip

        with VideoFileClip(file_path) as clip:
            return float(clip.duration)

    return await asyncio.to_thread(_read_duration)


async def _publish_video_processed_event(video_id: int) -> None:
    """Notify other services over Kafka that a video finished processing."""
    try:
        from aiokafka import AIOKafkaProducer

        producer = AIOKafkaProducer(bootstrap_servers=config.settings.kafka_broker)
        await producer.start()
        try:
            await producer.send_and_wait(
                config.settings.kafka_topic_video_processed,
                str(video_id).encode("utf-8"),
            )
        finally:
            await producer.stop()
    except Exception:
        logger.warning("Failed to publish video.processed event for video %s", video_id, exc_info=True)


async def _process_video(video_id: int, file_path: str) -> None:
    """Background task: derive video metadata and mark the video as processed."""
    async with async_session() as session:
        video = await session.get(models.Video, video_id)
        if video is None:
            return

        try:
            duration = await _extract_duration(file_path)
        except Exception:
            logger.exception("Failed to process video %s", video_id)
            return

        video.duration = duration
        video.is_processed = True
        video.updated_at = datetime.utcnow()
        session.add(
            models.VideoQuality(
                video_id=video.id,
                quality="original",
                file_path=file_path,
                bitrate="source",
            )
        )
        await session.commit()

    await _publish_video_processed_event(video_id)


@router.post("/upload", response_model=res.VideoUploadResponse)
async def upload_video(
    background_tasks: BackgroundTasks,
    video_upload: Annotated[req.VideoUploadRequest, Depends(_video_upload_form)],
    file: UploadFile = File(...),
    user_id: int = Depends(security.get_current_user_id),
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.VideoUploadResponse:
    """Upload a new video and schedule background processing."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}",
        )

    upload_dir = Path(config.settings.upload_dir)
    stored_filename = f"{uuid.uuid4().hex}{Path(file.filename).suffix}"
    file_path = upload_dir / stored_filename

    await _save_upload_file(file, file_path)

    video = models.Video(
        user_id=user_id,
        title=video_upload.title,
        description=video_upload.description,
        duration=0.0,
        original_file_path=str(file_path),
        is_processed=False,
        is_published=False,
    )
    session.add(video)
    await session.commit()
    await session.refresh(video)

    background_tasks.add_task(_process_video, video.id, str(file_path))

    return res.VideoUploadResponse(
        id=video.id,
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
