from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class PostgresSettings(BaseModel):
    database: str = "chat"
    user: str = "chat"
    password: str = "chat"
    host: str = "0.0.0.0"
    port: str = "5433"


class MongoSettings(BaseModel):
    user: str = "chat"
    password: str = "chat"
    host: str = "0.0.0.0"
    port: str = "27017"


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    mongo: MongoSettings = MongoSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
