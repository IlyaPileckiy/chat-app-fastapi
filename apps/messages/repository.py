from apps.chats.repository import ChatRepository
from apps.messages.models import Message, MessagesHistory
from core.models import PydanticObjectId
from core.mongo_client import database

collection = database.get_collection("messages")


class MessageRepository:
    collection = database.get_collection("messages")

    @staticmethod
    async def save_message(message: Message) -> Message:
        await ChatRepository.update_last_message(message)
        created = await collection.insert_one(message.dict())
        return Message.parse_obj(await collection.find_one({"_id": created.inserted_id}))

    @staticmethod
    async def get_chat_history(chat_id: PydanticObjectId, offset=0, limit=20) -> MessagesHistory:
        filter = {"chat_id": chat_id}
        sort = list({"created_at": -1}.items())
        total = await collection.count_documents(filter)
        query = collection.find(filter=filter, skip=offset).sort(sort).to_list(limit)
        messages = [Message.parse_obj(message) for message in await query]
        messages.reverse()

        return MessagesHistory(total=total, messages=messages)
