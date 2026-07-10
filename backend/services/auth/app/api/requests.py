from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegisterRequest(BaseModel):
    """Request model for user registration."""
    
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    
    username: str = Field(...)
    password: str = Field(...)


class UserUpdateRequest(BaseModel):
    """Request model for user update."""
    
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None


class ChangePasswordRequest(BaseModel):
    """Request model for changing password."""
    
    old_password: str = Field(...)
    new_password: str = Field(..., min_length=8)
