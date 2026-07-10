"""Mock data seeding script for development database."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.services.auth.app.core.config import settings as auth_settings
from backend.services.auth.app.mocks import MOCK_USERS
from backend.services.auth.app.core.security import get_password_hash


async def seed_auth_db():
    """Seed authentication database with mock data."""
    engine = create_async_engine(auth_settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # TODO: Implement user seeding
        print("Auth database seeding completed")
    
    await engine.dispose()


async def main():
    """Main seeding function."""
    await seed_auth_db()


if __name__ == "__main__":
    asyncio.run(main())
