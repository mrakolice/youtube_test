import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from sqlalchemy_declarative_extensions import register_alembic_events

register_alembic_events(schemas=True, roles=True, grants=True, rows=True)

# Add your model's MetaData object for 'autogenerate' support
from app.db.base import Base

target_metadata = Base.metadata

database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://youtube_user:youtube_password@localhost:5432/youtube_db")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        url = database_url
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    if not configuration.get("sqlalchemy.url"):
        configuration["sqlalchemy.url"] = database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(lambda sync_conn: context.configure(connection=sync_conn, target_metadata=target_metadata))
            async with connection.begin():
                await connection.run_sync(lambda sync_conn: context.run_migrations())

    asyncio.run(run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
