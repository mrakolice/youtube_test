from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model for authentication service."""
    
    __tablename__ = "users"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(Integer),
    )
    username: str = Field(
        index=True,
        unique=True,
        max_length=50,
        sa_column=Column(String(50), nullable=False),
    )
    email: str = Field(
        index=True,
        unique=True,
        max_length=100,
        sa_column=Column(String(100), nullable=False),
    )
    hashed_password: str = Field(
        max_length=255,
        sa_column=Column(String(255), nullable=False),
    )
    first_name: Optional[str] = Field(
        default=None,
        max_length=50,
        sa_column=Column(String(50)),
    )
    last_name: Optional[str] = Field(
        default=None,
        max_length=50,
        sa_column=Column(String(50)),
    )
    is_active: bool = Field(
        default=True,
        sa_column=Column(Integer, default=1),
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )

    class Config:
        arbitrary_types_allowed = True
