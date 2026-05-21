from fastapi import Request, HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel
from .schemas import CreateUserSchema, LoginSchema
from src.utils.password_hasher import password_hasher


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_user_by_id(self, user_id: int) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalars().one_or_none()

    async def _get_user_by_phone(self, phone_number: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.phone_number == phone_number)
        )
        return result.scalars().one_or_none()

    async def _get_user_by_username(self, username: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalars().one_or_none()

    async def create_user(self, user: CreateUserSchema) -> UserModel:
        if await self._get_user_by_phone(user.phone_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this phone number already exists",
            )

        data = user.model_dump()
        data["password"] = password_hasher.hash(data["password"])

        new_user = UserModel(**data)

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def authenticate_user(self, login_data: LoginSchema) -> UserModel:
        user = await self._get_user_by_id
