from internal.dto.application import (
    ApplicationOut,
    CreateApplicationDTO,
    GetApplicationDTO,
    UpdateApplicationDTO,
)
from internal.repositories.application import ApplicationRepository


class ApplicationService:
    def __init__(self, repo: ApplicationRepository) -> None:
        self.repo = repo

    async def get_one(self, data: GetApplicationDTO) -> ApplicationOut:
        return await self.repo.get_one(data.model_dump(exclude_none=True))

    async def get_many(self, data: GetApplicationDTO) -> list[ApplicationOut]:
        return await self.repo.get_many(data.model_dump(exclude_none=True))

    async def create(self, data: CreateApplicationDTO) -> ApplicationOut:
        payload = data.model_dump(exclude_none=True)
        if 'screenshots' not in payload:
            payload['screenshots'] = []
        return await self.repo.create(payload)

    async def update(self, item_id: int, data: UpdateApplicationDTO) -> ApplicationOut:
        return await self.repo.update(item_id, data.model_dump(exclude_none=True))

    async def delete(self, item_id: int) -> None:
        await self.repo.delete(item_id)

