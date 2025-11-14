import re
from typing import Literal

from sqlalchemy.sql.schema import SchemaItem

from internal.repositories.db.helpers import create_dsn
from internal.repositories.db.models import BaseOrm

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine


target_metadata = BaseOrm.metadata

config = context.config


config.set_main_option('sqlalchemy.url', create_dsn())
SA_TYPE = Literal["schema", "table", "column", "index", "unique_constraint", "foreign_key_constraint"]


def include_object(object: SchemaItem, name: str | None, type_: SA_TYPE, reflected: bool, compare_to: SchemaItem | None, ) -> bool:
    if type_ == 'table' and re.match('directus.*', name):
        return False

    return True


def run_migrations_offline():
    """Запуск миграций в оффлайн режиме."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций в онлайн режиме."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())