from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings for video service."""
    
    database_url: str = "postgresql+asyncpg://youtube_user:youtube_password@localhost:5432/youtube_db?schema=videos"
    redis_url: str = "redis://:redis_password@localhost:6379"
    
    # JWT Configuration
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    
    # Service URLs
    auth_service_url: str = "http://localhost:8001"
    
    # Kafka
    kafka_broker: str = "localhost:9092"
    kafka_topic_video_processed: str = "video.processed"
    
    # Video processing
    max_upload_size: int = 5 * 1024 * 1024 * 1024  # 5GB
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
