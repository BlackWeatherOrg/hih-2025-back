from contextlib import asynccontextmanager
from typing import AsyncContextManager, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
    """Database connection/session manager"""
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[sessionmaker[AsyncSession]] = None


    def get_engine(self) -> AsyncEngine:
        return self._engine

    def get_sessionmaker(self) -> sessionmaker[AsyncSession]:
        return self._sessionmaker

    def init(self, dsn: str, poolclass=None) -> None:
        """DatabaseManager'a initialization

        Args:
            dsn: DSN string to connect to database
            poolclass:

        Returns:

        """
        connect_args = {}
        if 'postgresql' in dsn:
            connect_args.update(
                {
                    'statement_cache_size': 0,
                    'prepared_statement_cache_size': 0,
                }
            )

        self._engine = create_async_engine(
            url=dsn,
            pool_pre_ping=True,
            connect_args=connect_args,
            poolclass=poolclass,
            echo=False,
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncContextManager[AsyncSession]:
        if self._sessionmaker is None:
            raise IOError('DatabaseSessionManager is not initialized')
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e


db_manager = DatabaseManager()


async def get_session() -> AsyncContextManager[AsyncSession]:
    async with db_manager.session() as session:
        yield session