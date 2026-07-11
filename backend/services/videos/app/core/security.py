from typing import Optional

from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

from app.core import config


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token issued by the auth service."""
    try:
        payload = jwt.decode(
            token,
            config.settings.jwt_secret_key,
            algorithms=[config.settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        raise ValueError("Invalid token")


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    """Extract and validate the current user id from the Authorization header.

    The video service does not manage users itself; it trusts the JWT
    issued by the auth service (both services share ``jwt_secret_key``).
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user id",
        )

    return int(user_id)
