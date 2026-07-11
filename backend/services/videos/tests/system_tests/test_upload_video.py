from sqlalchemy import select

from app import models


async def test_upload_video_requires_authentication(client, sample_mp4_bytes):
    response = await client.post(
        "/api/videos/upload",
        data={"title": "No auth video"},
        files={"file": ("clip.mp4", sample_mp4_bytes, "video/mp4")},
    )

    assert response.status_code == 401


async def test_upload_video_rejects_unsupported_content_type(client, make_token):
    response = await client.post(
        "/api/videos/upload",
        headers={"Authorization": f"Bearer {make_token()}"},
        data={"title": "Wrong type"},
        files={"file": ("clip.txt", b"not a video", "text/plain")},
    )

    assert response.status_code == 400


async def test_upload_video_persists_and_processes_in_background(
    client, make_token, sample_mp4_bytes, db_session_factory
):
    response = await client.post(
        "/api/videos/upload",
        headers={"Authorization": f"Bearer {make_token(user_id=7)}"},
        data={"title": "My great video", "description": "A short clip"},
        files={"file": ("clip.mp4", sample_mp4_bytes, "video/mp4")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["upload_status"] == "processing"
    video_id = body["id"]

    async with db_session_factory() as session:
        video = await session.get(models.Video, video_id)
        assert video is not None
        assert video.user_id == 7
        assert video.title == "My great video"
        assert video.description == "A short clip"
        # The background task runs to completion before the ASGI response
        # cycle returns control to the test client, so processing is done here.
        assert video.is_processed is True
        assert video.duration > 0

        qualities = (
            await session.execute(
                select(models.VideoQuality).where(models.VideoQuality.video_id == video_id)
            )
        ).scalars().all()
        assert any(quality.quality == "original" for quality in qualities)
