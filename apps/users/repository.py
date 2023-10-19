from apps.users.models import UserModel
from apps.users.queries import USER_LIST_QUERY, USER_QUERY

from core.postgres_client import Database


class UsersRepository:
    def __init__(self, database: Database) -> None:
        self._pg = database

    async def get_users_list(self, ids) -> list[UserModel]:
        return [
            UserModel(**row) for row in await self._pg.pool.fetch(USER_LIST_QUERY, ids)
        ]

    async def get_user(self, user_id: int) -> UserModel | None:
        user = await self._pg.pool.fetchrow(USER_QUERY, user_id)
        if not user:
            return None
        return UserModel(**user)
