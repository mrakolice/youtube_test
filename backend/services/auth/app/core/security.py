from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt import PyJWTError
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from app.core import config

# Bcrypt explicitly rather than PasswordHash.recommended() (Argon2): the users
# table already holds $2b$ hashes written by the previous passlib-based code,
# and those must keep verifying.
pwd_hash = PasswordHash((BcryptHasher(),))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash."""
    return pwd_hash.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.settings.jwt_access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.settings.jwt_secret_key,
        algorithm=config.settings.jwt_algorithm,
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(
            token,
            config.settings.jwt_secret_key,
            algorithms=[config.settings.jwt_algorithm],
        )
        return payload
    except PyJWTError:
        raise ValueError("Invalid token")
