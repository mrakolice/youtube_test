import enum

from sqlmodel import Field, SQLModel


class UrlAccess(enum.StrEnum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class Urls(SQLModel, table=True):
    __tablename__ = 'urls'

    id: int = Field(primary_key=True)
    url: str = Field(index=True)
    rate_limit: int = Field(default=1)
    access: str = Field(default=UrlAccess.PRIVATE)
