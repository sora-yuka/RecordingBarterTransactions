from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.barter.models import BarterModel
from src.apps.barter.schemas import *


class BarterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_object(self, id: int) -> BarterModel:
        result = await self.session.execute(
            select(BarterModel).where(BarterModel.id == id)
        )
        return result.scalars().one_or_none()

    async def get_objects(self) -> BarterModel:
        result = await self.session.execute(select(BarterModel))
        return result.scalars()

    async def create_object(self, data: CreateBarterSchema) -> BarterModel:
        barter = BarterModel(**data)
        self.session.add(barter)
        await self.session.commit()
        await self.session.refresh(barter)
        return barter

    async def update_object(self, id: int, data: UpdateBarterSchema) -> BarterModel:
        barter = data.model_dump(exclude_unset=True)
        await self.session.execute(
            update(BarterModel).where(BarterModel.id == id).values(**barter)
        )
        await self.session.commit()
        result = await self.get_object(id)
        return result

    async def delete_object(self, id: int) -> None:
        await self.session.execute(delete(BarterModel).where(BarterModel.id == id))
        await self.session.commit()
