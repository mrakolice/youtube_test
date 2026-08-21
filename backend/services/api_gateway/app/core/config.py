import pathlib

import pydantic_settings


class PostgresSettings(pydantic_settings.BaseSettings):
    database: str
    host: str
    port: int
    user: str
    password: str

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


class KafkaSettings(pydantic_settings.BaseSettings):
    url: str


class RedisSettings(pydantic_settings.BaseSettings):
    url: str


class RabbitMQSettings(pydantic_settings.BaseSettings):
    url: str


class ServicesSettings(pydantic_settings.BaseSettings):
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

    model_config = pydantic_settings.SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter='__',
    )

env_file = pathlib.Path(__file__).parent.parent.parent.joinpath('.env')

config = Config(_env_file=env_file)
