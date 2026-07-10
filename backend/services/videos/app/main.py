from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.views import router as video_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="YouTube Video Service",
    description="Video management service for YouTube clone",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(video_router)


@app.on_event("startup")
async def startup() -> None:
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
