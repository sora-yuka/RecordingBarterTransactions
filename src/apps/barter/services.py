from src.apps.barter.dependencies import RepositoryDep
from src.apps.barter.schemas import *


class BarterService:
    def __init__(self, repo: RepositoryDep):
        self.repo = repo

    async def get_barters(self) -> list[ReadBarterSchema]:
        results = await self.repo.get_objects()
        return [ReadBarterSchema.model_validate(r) for r in results]

    async def get_barter_by_id(self, barter_id: int) -> ReadBarterSchema | None:
        result = await self.repo.get_object(barter_id)
        return ReadBarterSchema.model_validate(result)

    async def create(self, data: CreateBarterSchema) -> ReadBarterSchema:
        data = data.model_dump()
        result = await self.repo.create_object(data)
        return ReadBarterSchema.model_validate(result)

    async def update(self, id: int, data: UpdateBarterSchema) -> ReadBarterSchema:
        data = data.model_dump(exclude_unset=True)
        result = await self.repo.update_object(id, data)
        return ReadBarterSchema.model_validate(result)

    async def delete(self, id: int) -> None:
        await self.repo.delete_object(id)
