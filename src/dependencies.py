from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config.database import AsyncSession, get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

CredentialsDep = Annotated[
    HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))
]
