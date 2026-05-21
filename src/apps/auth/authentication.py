from typing import Optional
from datetime import timedelta, datetime, timezone

from jose import JWTError, jwt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer

from src.config.settings import settings

oauth2_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def raise_401_status(detail: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def decode_token(token: str, expected_type: str = "access") -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except JWTError:
        raise_401_status("Cound not validate credentials")

    if payload.get("sub") is None:
        raise_401_status("Cound not validate credentials")
    if payload.get("type") != expected_type:
        raise_401_status(f"Expected a {expected_type} token")
    return payload
