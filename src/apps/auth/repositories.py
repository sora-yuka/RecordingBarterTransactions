from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_field(self, **kwargs) -> UserModel | None:
        if not kwargs:
            return None
        filters = [getattr(UserModel, key) == val for key, val in kwargs.items()]
        result = await self.session.execute(select(UserModel).where(*filters))
        return result.scalars().one_or_none()

    async def create(self, data: dict) -> UserModel:
        user = UserModel(**data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
