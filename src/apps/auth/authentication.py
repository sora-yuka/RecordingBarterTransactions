from enum import Enum
from datetime import timedelta, datetime, timezone

from jose import ExpiredSignatureError, JWTError, jwt

from .exceptions import TokenExpiredException, InvalidTokenException
from src.config.settings import settings


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def create_jwt_token(
    data: dict, expires_delta: timedelta, token_type: TokenType
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type.value})
    return jwt.encode(to_encode, settings.secret_key_str, algorithm=settings.ALGORITHM)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    delta = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_jwt_token(data, delta, TokenType.ACCESS)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    delta = expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_jwt_token(data, delta, TokenType.REFRESH)


def decode_token(token: str, expected_type: TokenType = TokenType.ACCESS) -> dict:
    try:
        payload = jwt.decode(
            token, settings.secret_key_str, algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        raise TokenExpiredException("Token has expired")
    except JWTError:
        raise InvalidTokenException("Could not validate credentials")

    if not payload.get("sub"):
        raise InvalidTokenException("Could not validate credentials")

    if payload.get("type") != expected_type.value:
        raise InvalidTokenException(f"Expected a {expected_type.value} token")

    return payload
