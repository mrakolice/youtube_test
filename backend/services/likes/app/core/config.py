from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for like service."""
    
    database_url: str = "postgresql+asyncpg://youtube_user:youtube_password@localhost:5432/youtube_db?schema=likes"
    redis_url: str = "redis://:redis_password@localhost:6379"
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    kafka_broker: str = "localhost:9092"
    kafka_topic_like_recorded: str = "like.recorded"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
