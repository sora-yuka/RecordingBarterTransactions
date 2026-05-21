from fastapi import APIRouter

from .dependencies import ServiceDep, CurrentUserDep
from .authentication import create_access_token, create_refresh_token
from .schemas import CreateUserSchema, ReadUserSchema, LoginSchema, TokenSchema

router = APIRouter()


@router.post("/register", response_model=ReadUserSchema)
async def register_user(user: CreateUserSchema, service: ServiceDep):
    return await service.create_user(user)


@router.post("/login", response_model=TokenSchema)
async def login_user(login_data: LoginSchema, service: ServiceDep):
    user = await service.authenticate_user(login_data)
    token_payload = {"sub": str(user.id)}
    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=ReadUserSchema)
async def get_me(current_user: CurrentUserDep):
    return current_user
