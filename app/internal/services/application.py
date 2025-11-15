import config
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
        application: ApplicationOut = await self.repo.get_one(data.model_dump(exclude_none=True))
        if application.id % 2 != 0 or application.name == 'ВКонтакте: чаты, видео, музыка':
            application.apk_link = f'{config.APK_HOSTNAME}{config.APK_PATH}vkontakte-chaty-video-muzyka.apk'
        else:
            application.apk_link = f'{config.APK_HOSTNAME}{config.APK_PATH}vk-video-kino-serialy-tv-i.apk'
        return await self.repo.get_one(data.model_dump(exclude_none=True))

    async def get_many(self, data: GetApplicationDTO) -> list[ApplicationOut]:
        applications: list[ApplicationOut] = await self.repo.get_many(data.model_dump(exclude_none=True))
        for appl in applications:
            if appl.id % 2 != 0 or appl.name == 'ВКонтакте: чаты, видео, музыка':
                appl.apk_link = 'http://localhost:7070/api/static/apks/vkontakte-chaty-video-muzyka.apk'
            else:
                appl.apk_link = 'http://localhost:7070/api/static/apks/vk-video-kino-serialy-tv-i.apk'
        return applications

    async def create(self, data: CreateApplicationDTO) -> ApplicationOut:
        payload = data.model_dump(exclude_none=True)
        if 'screenshots' not in payload:
            payload['screenshots'] = []
        return await self.repo.create(payload)

    async def update(self, item_id: int, data: UpdateApplicationDTO) -> ApplicationOut:
        return await self.repo.update(item_id, data.model_dump(exclude_none=True))

    async def delete(self, item_id: int) -> None:
        await self.repo.delete(item_id)

