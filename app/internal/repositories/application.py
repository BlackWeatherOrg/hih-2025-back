from sqlalchemy import select

from internal.repositories.db.base import BaseSQLAlchemyRepository
from internal.repositories.db.models.application import Application


class ApplicationRepository(BaseSQLAlchemyRepository):
    model = Application

    async def get_many(self, data: dict) -> list:
        return_in_order = data.pop('return_in_order', None)
        offset = data.pop('offset', None)
        limit = data.pop('limit', None)
        name_filter = data.pop('name', None)
        data = self._normalize_payload(data)
        query = select(self.model)
        if name_filter is not None:
            query = query.filter(self.model.name.ilike(f'%{name_filter}%'))
        if data:
            query = query.filter_by(**data)
        if return_in_order:
            query = query.order_by(self.model.id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self._execute_query(query)
        return [item.to_dto() for item in result.scalars().all()]

    async def create(self, data: dict):
        screenshots = data.get('screenshots')
        if screenshots is None:
            data = {**data, 'screenshots': []}
        return await super().create(data)

    async def update(self, item_id: int, data: dict):
        if 'screenshots' in data and data['screenshots'] is None:
            data['screenshots'] = []
        return await super().update(item_id, data)

