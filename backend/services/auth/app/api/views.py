from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api import requests as req
from app.api import responses as res
from app.core import config, security
from app.db.session import get_db

from app import models

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=res.RegisterResponse)
async def register(
    registration_data: req.UserRegisterRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> res.RegisterResponse:
    """Register a new user."""
    # Check if user already exists
    existing_user = await session.execute(
        sa.select(models.User).filter(
            sa.or_(
                models.User.email==registration_data.email,
                models.User.username==registration_data.username,
            )
        )
    )
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )
    
    # Create new user
    hashed_password = security.get_password_hash(registration_data.password)
    new_user = models.User(
        username=registration_data.username,
        email=registration_data.email,
        hashed_password=hashed_password,
        first_name=registration_data.first_name,
        last_name=registration_data.last_name,
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return res.RegisterResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
    )


@router.post("/login", response_model=res.LoginResponse)
async def login(
    login_data: req.UserLoginRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> res.LoginResponse:
    """Authenticate user and return access token."""
    # Find user by username
    user = await session.query(models.User).filter(models.User.username == login_data.username).one_or_none()

    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Create access token
    access_token = security.create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=timedelta(minutes=config.settings.jwt_access_token_expire_minutes),
    )
    
    user_response = res.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    
    return res.LoginResponse(
        access_token=access_token,
        user=user_response,
    )


@router.get("/me", response_model=res.UserResponse)
async def get_current_user(
    token: str = Depends(security.decode_token),
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.UserResponse:
    """Get current authenticated user."""
    if not token or "sub" not in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    user_id = int(token["sub"])
    result = await session.execute(
        "SELECT * FROM users WHERE id = :id",
        {"id": user_id},
    )
    user = result.scalar()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return res.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/me", response_model=res.UserResponse)
async def update_current_user(
    update_data: req.UserUpdateRequest,
    token: str = Depends(security.decode_token),
    session: Annotated[AsyncSession, Depends(get_db)] = None,
) -> res.UserResponse:
    """Update current authenticated user."""
    if not token or "sub" not in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    user_id = int(token["sub"])
    result = await session.execute(
        "SELECT * FROM users WHERE id = :id",
        {"id": user_id},
    )
    user = result.scalar()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update user fields
    if update_data.first_name is not None:
        user.first_name = update_data.first_name
    if update_data.last_name is not None:
        user.last_name = update_data.last_name
    if update_data.email is not None:
        user.email = update_data.email
    
    await session.commit()
    await session.refresh(user)
    
    return res.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
