from typing import Optional
import asyncpg
import logging

from core.settings import get_settings

settings = get_settings()
logger = logging.getLogger()


class Database:
    """
    Initial data base class for open connections pool and store it
    """

    def __init__(self) -> None:
        self._pool: Optional[asyncpg.Pool] = None

    @property
    def pool(self):
        assert self._pool is not None
        return self._pool

    async def close_pool(self):
        assert self._pool is not None
        await self._pool.close()
        logger.info("Database pool is closed")

    async def create_pool(self):
        self._pool = await asyncpg.create_pool(
            database=settings.postgres.database,
            user=settings.postgres.user,
            password=settings.postgres.password,
            host=settings.postgres.host,
            port=settings.postgres.port,
        )
        logger.info("Database pool is opened")


database = Database()
