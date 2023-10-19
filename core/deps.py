from typing import Generator
from core.settings import get_settings
from core.postgres_client import Database, database

settings = get_settings()


def get_db() -> Generator[Database, None, None]:
    yield database
