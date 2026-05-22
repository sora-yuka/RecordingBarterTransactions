from typing import Annotated

from fastapi import Depends

from .services import UserService
from src.dependencies import SessionDep


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


ServiceDep = Annotated[UserService, Depends(get_user_service)]
