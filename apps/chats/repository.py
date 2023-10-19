from itertools import chain
from typing import List, Optional

from bson.objectid import ObjectId

from apps.chats.models import Chat, HistoryChats
from apps.users.repository import UsersRepository
from core.mongo_client import database as mongo_database

collection = mongo_database.get_collection("chats")


class ChatRepository:
    @staticmethod
    async def get_chat_by_id(chat_id: ObjectId) -> Chat:
        return Chat.parse_obj(await collection.find_one({"_id": chat_id}))

    @classmethod
    async def get_chat_by_memebers(cls, db, sender_id: int, members: List[int]) -> Chat:
        chat = await collection.find_one({"members": sorted(members)})
        if not chat:
            created = await collection.insert_one({"members": members})
            chat = await collection.find_one({"_id": created.inserted_id})

        chat = Chat.parse_obj(chat)

        receiver_id = cls.get_receiver_id(sender_id, chat.members)
        assert receiver_id

        profile = await UsersRepository(database=db).get_user(receiver_id)
        assert profile

        chat.name = cls.get_chat_name(profile)
        return chat

    @classmethod
    async def get_users_chats(cls, db, user_id, offset=0, limit=10) -> HistoryChats:
        filter = {"members": {"$in": [user_id]}}
        sort = list({"last_message": -1}.items())
        total = await collection.count_documents(filter)
        query = collection.find(filter=filter, skip=offset).sort(sort).to_list(limit)
        chats: List[Chat] = [Chat.parse_obj(chat) for chat in await query]
        chats.reverse()
        await cls.add_info_for_chats(db, chats, user_id)

        return HistoryChats(total=total, chats=chats)

    @staticmethod
    def get_receiver_id(sender_id: int, members: List[int]) -> Optional[int]:
        members_without_user = members[:]
        members_without_user.remove(sender_id)
        if members_without_user:
            return members_without_user[0]

    @staticmethod
    def get_chat_name(profile) -> str:
        if profile.first_name or profile.last_name:
            return f"{profile.first_name} {profile.last_name}"
        return profile.email

    @classmethod
    async def add_info_for_chats(cls, db, chats: List[Chat], user_id) -> None:
        members = tuple(set(chain(*[chat.members for chat in chats])))

        result = await UsersRepository(database=db).get_users_list(members)

        for chat in chats:
            if not chat.name:
                name = "Без имени"
                member_id = cls.get_receiver_id(user_id, chat.members)
                member_profiles = [user for user in result if user.id == member_id]
                if member_profiles:
                    member_profile = member_profiles[0]
                    name = cls.get_chat_name(member_profile)
                chat.name = name if not chat.name else chat.name

    @staticmethod
    async def update_last_message(message):
        return await collection.update_one(
            {"_id": message.chat_id},
            {
                "$set": {
                    "last_message": {"date": message.created_at, "text": message.text}
                }
            },
        )
