from fastapi import APIRouter

from src.dependencies import SessionDep
from .schemas import CreateUserSchema, ReadUserSchema
from .dependencies import ServiceDep

router = APIRouter()

@router.post("/register", response_model=ReadUserSchema)
async def create_user(user: CreateUserSchema, service: ServiceDep):
    return await service.create_user(user)
