import subprocess
from typing import AsyncGenerator, Callable

import imageio_ffmpeg
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app import models  # noqa: F401  (registers Video/VideoQuality on SQLModel.metadata)
from app.api import views
from app.core import config
from app.db.session import get_db
from app.main import app as fastapi_app


@pytest_asyncio.fixture
async def db_session_factory() -> AsyncGenerator[sessionmaker, None]:
    """An isolated in-memory SQLite database, fresh for every test."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield session_factory

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session_factory, tmp_path, monkeypatch) -> AsyncGenerator[AsyncClient, None]:
    """An async HTTP client wired to the isolated DB and a scratch upload directory."""
    monkeypatch.setattr(config.settings, "upload_dir", str(tmp_path / "uploads"))
    # The background processing task in views.py resolves `async_session` as a
    # module global, so it must be patched there to use the isolated test DB.
    monkeypatch.setattr(views, "async_session", db_session_factory)

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with db_session_factory() as session:
            yield session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client

    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def make_token() -> Callable[..., str]:
    """Factory for signing JWTs the same way the auth service would."""

    def _make(user_id: int = 1) -> str:
        return jwt.encode(
            {"sub": str(user_id), "username": "tester"},
            config.settings.jwt_secret_key,
            algorithm=config.settings.jwt_algorithm,
        )

    return _make


@pytest.fixture(scope="session")
def sample_mp4_bytes(tmp_path_factory) -> bytes:
    """Render a tiny, real mp4 once per test session so duration extraction has real data to read."""
    output_path = tmp_path_factory.mktemp("fixtures") / "sample.mp4"
    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-f", "lavfi",
            "-i", "testsrc=duration=1:size=32x32:rate=5",
            "-pix_fmt", "yuv420p",
            "-y", str(output_path),
        ],
        check=True,
        capture_output=True,
    )
    return output_path.read_bytes()
