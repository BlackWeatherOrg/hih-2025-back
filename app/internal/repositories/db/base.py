import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from sqlalchemy import select, update, delete, Result
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from internal.core.exceptions import NotFoundError, AlreadyExistException
from internal.repositories.db.manager import db_manager


class BaseDBRepository(ABC):
    """Базовый абстрактный репозиторий для работы с отдельно взятой таблицей БД"""

    model = NotImplemented
    session = db_manager.session

    @abstractmethod
    async def get_one(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_many(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    async def _execute_query(self, query, commit: bool = False) -> Result:
        async with self.session() as session:
            result = await session.execute(query)
            if commit:
                await session.commit()
        return result

    async def get_by_ids(self, model, ids: list) -> list:
        query = select(model).filter(model.id.in_(ids))

        result = await self._execute_query(query)
        return [item for item in result.scalars().all()]


class BaseSQLAlchemyRepository(BaseDBRepository):
    @staticmethod
    def _normalize_value(value):
        if isinstance(value, datetime):
            # Convert timezone-aware datetime to naive UTC to match TIMESTAMP WITHOUT TIME ZONE
            if value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None:
                return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    @classmethod
    def _normalize_payload(cls, data: dict) -> dict:
        return {k: cls._normalize_value(v) for k, v in data.items()}

    async def get_one(self, data: dict):
        data.pop('return_in_order')
        data = self._normalize_payload(data)
        query = select(self.model).filter_by(**data)
        result = await self._execute_query(query)
        item = result.scalar_one_or_none()

        if not item:
            raise NotFoundError

        return item.to_dto()

    async def get_many(self, data: dict):
        data = self._normalize_payload(data)
        query = select(self.model).filter_by(**data)
        result = await self._execute_query(query)
        items = result.scalars().all()

        return [item.to_dto() for item in items]

    async def create(self, data: dict):
        data = self._normalize_payload(data)
        query = insert(self.model).values(**data).returning(self.model)

        try:
            result = await self._execute_query(query, commit=True)
        except IntegrityError:
            raise AlreadyExistException
        item = result.scalar_one()

        return item.to_dto()

    async def update(self, item_id: uuid.UUID, data: dict):
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data = self._normalize_payload(update_data)

        if not update_data:
            return await self.get_one({'id': item_id})

        query = update(self.model).where(self.model.id == item_id).values(**update_data).returning(self.model)
        result = await self._execute_query(query, commit=True)
        item = result.scalar_one_or_none()

        if not item:
            raise NotFoundError

        return item.to_dto()

    async def delete(self, item_id: uuid.UUID) -> None:
        check_query = select(self.model).where(self.model.id == item_id)
        result = await self._execute_query(check_query)
        item = result.scalar_one_or_none()

        if not item:
            raise NotFoundError

        query = delete(self.model).where(self.model.id == item_id)
        await self._execute_query(query, commit=True)
