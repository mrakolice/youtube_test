import pydantic
import pydantic_settings


class PostgresSettings(pydantic_settings.BaseSettings):
    host: str
    port: int
    user: str
    password: str


class KafkaSettings(pydantic_settings.BaseSettings):
    url: str


class RedisSettings(pydantic_settings.BaseSettings):
    url: str


class RabbitMQSettings(pydantic_settings.BaseSettings):
    url: str


class ServicesSettings:
    auth_url: str
    videos_url: str
    likes_url: str
    views_url: str


class Config(pydantic_settings.BaseSettings):
    postgres: PostgresSettings
    kafka: KafkaSettings
    redis: RedisSettings
    rabbitmq: RabbitMQSettings
    services: ServicesSettings

    model_config = pydantic.SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
    )


config = Config()
