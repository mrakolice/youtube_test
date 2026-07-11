FROM python:3.11-slim

ARG UID=1000
ARG GID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv \
    # Non-root user matching the host UID/GID that owns the bind-mounted
    # source tree, so files created inside the container (.venv, egg-info,
    # __pycache__, ...) are never owned by root on the host.
    && groupadd --gid "${GID}" appuser \
    && useradd --uid "${UID}" --gid "${GID}" --create-home --shell /bin/bash appuser

WORKDIR /app
RUN chown appuser:appuser /app
USER appuser

# Install third-party dependencies in their own layer first so editing
# application code doesn't bust the dependency install cache.
COPY --chown=appuser:appuser pyproject.toml uv.lock* ./
RUN uv sync --no-install-project

COPY --chown=appuser:appuser . .
RUN uv sync

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8001"]
