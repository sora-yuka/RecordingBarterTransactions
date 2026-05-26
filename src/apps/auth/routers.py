from fastapi import APIRouter

from src.apps.auth.schemas import ReadUserSchema, AuthorizeUserSchema, TokenSchema
from src.apps.auth.dependencies import UserServiceDep, AuthServiceDep, UserFormDep, CredentialsDep, CurrentUserDep

router = APIRouter()


@router.post("/enroll", response_model=ReadUserSchema)
async def enroll(service: UserServiceDep, form_data: UserFormDep):
    return await service.create_user(form_data)


@router.post("/authorize", response_model=TokenSchema)
async def authorize(service: AuthServiceDep, json_data: AuthorizeUserSchema):
    return await service.authenticate_user(json_data)


@router.post("/refresh")
async def refresh(service: AuthServiceDep, headers: CredentialsDep):
    return await service.refresh_user_tokens(headers.credentials)


@router.get("/", response_model=ReadUserSchema)
async def get_me(current_user: CurrentUserDep):
    return current_user
