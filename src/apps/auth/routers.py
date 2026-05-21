from fastapi import APIRouter

from .schemas import CreateUserSchema, ReadUserSchema
from .dependencies import ServiceDep, CurrentUserDep

router = APIRouter()


@router.post("/register", response_model=ReadUserSchema)
async def create_user(user: CreateUserSchema, service: ServiceDep):
    return await service.create_user(user)


# @router.post("/login", response_model=ReadUserSchema)
# async def read_user(user)


@router.get("/me", response_model=ReadUserSchema)
async def get_me(current_user: CurrentUserDep):
    return current_user
