from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.sql.elements import KeyedColumnElement


class BaseOrm(DeclarativeBase, AsyncAttrs):
    __table_args__ = {'schema': 'public'}

    @classmethod
    def columns(cls) -> Callable[[], ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]]:
        return cls.__table__.columns

    def to_dto(self):
        raise NotImplementedError()
