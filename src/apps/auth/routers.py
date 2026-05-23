from fastapi import APIRouter, HTTPException, status

from .dependencies import ServiceDep, UserRegisterFormDep
from .schemas import ReadUserSchema, AuthorizeUserSchema, TokenSchema
from .exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from src.dependencies import CredentialsDep

router = APIRouter()


@router.post("/register", response_model=ReadUserSchema)
async def register(user: UserRegisterFormDep, service: ServiceDep):
    try:
        return await service.create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenSchema)
async def login(data: AuthorizeUserSchema, service: ServiceDep):
    try:
        user = await service.authenticate_user(data)
        return service.generate_tokens(user.id, user.phone_number)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenSchema)
async def refresh(credentials: CredentialsDep, service: ServiceDep):
    try:
        return await service.refresh_user_tokens(credentials.credentials)
    except InvalidTokenException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=ReadUserSchema)
async def get_me(credentials: CredentialsDep, service: ServiceDep):
    return await service.get_current_user(credentials.credentials)
