from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.barter.models import BarterModel


class BarterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_object(self, id: int) -> BarterModel | None:
        result = await self.session.execute(
            select(BarterModel).where(BarterModel.id == id)
        )
        return result.scalars().one_or_none()

    async def get_objects(self) -> Sequence[BarterModel]:
        result = await self.session.execute(select(BarterModel))
        return result.scalars().all()

    async def create_object(self, data: dict) -> BarterModel:
        barter = BarterModel(**data)
        self.session.add(barter)
        await self.session.commit()
        await self.session.refresh(barter)
        return barter

    async def update_object(self, id: int, data: dict) -> BarterModel:
        if data:
            await self.session.execute(
                update(BarterModel).where(BarterModel.id == id).values(**data)
            )
            await self.session.commit()
        return await self.get_object(id)

    async def delete_object(self, id: int) -> None:
        await self.session.execute(delete(BarterModel).where(BarterModel.id == id))
        await self.session.commit()
