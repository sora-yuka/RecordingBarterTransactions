from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from .models import UserModel
from .services import UserService
from .authentication import oauth2_scheme, decode_token, raise_401_status
from src.dependencies import SessionDep


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


ServiceDep = Annotated[UserService, Depends(get_user_service)]

TokenDep = Annotated[HTTPAuthorizationCredentials | None, Depends(oauth2_scheme)]


async def get_current_user(token_auth: TokenDep, user_service: ServiceDep) -> UserModel:
    if not token_auth:
        raise_401_status("Missing or malformed Authorization header")
    payload = decode_token(token_auth.credentials, expected_type="access")
    user_id = payload.get("sub")
    user = await user_service._get_user_by_id(user_id)
    if not user:
        raise_401_status("User not found")
    return user


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
