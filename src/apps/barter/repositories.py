from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.barter.models import BarterModel


class BarterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_barter_by_id(self, id: int) -> BarterModel:
        result = await self.session.execute(
            select(BarterModel).where(BarterModel.id == id)
        )
        return result.scalars()

    async def create(self, data: dict) -> BarterModel:
        barter = BarterModel(**data)
        self.session.add(barter)
        await self.session.commit()
