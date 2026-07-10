from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str = "postgresql+asyncpg://youtube_user:youtube_password@localhost:5432/youtube_db"
    redis_url: str = "redis://:redis_password@localhost:6379"
    
    # JWT Configuration
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # Service URLs
    auth_service_url: str = "http://localhost:8001"
    video_service_url: str = "http://localhost:8002"
    view_service_url: str = "http://localhost:8003"
    like_service_url: str = "http://localhost:8004"
    
    # Kafka
    kafka_broker: str = "localhost:9092"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
