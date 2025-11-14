import config


def create_dsn():
    return (
        f'postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}'
        f'@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}'
    )
