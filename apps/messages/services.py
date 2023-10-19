import json
import logging
from datetime import datetime

from apps.chats.repository import ChatRepository

from apps.messages.models import Message, MessageAction, MessageRequest
from apps.messages.repository import MessageRepository


wb_logger = logging.getLogger("uvicorn")


async def send_message(message, ids, connections_manager) -> None:
    for receiver_id in ids:
        receivier = await connections_manager.get_receiver(receiver_id)
        if receivier:
            await receivier.send_json(message)


async def process_new_message(message_data, user_id, connections_manager) -> None:
    data = MessageRequest.parse_obj(message_data)
    wb_logger.warning(f"Message: {data.text} # {user_id} -> {data.chat_id}")

    chat = await ChatRepository.get_chat_by_id(data.chat_id)

    assert user_id in chat.members, "Пользователя нет в этом чате"

    message = await MessageRepository.save_message(
        Message(
            sender=user_id,
            created_at=datetime.now(),
            is_read=False,
            **data.dict()
        )
    )

    json_message = json.loads(MessageAction(data=message).json())
    json_message['data']['temp_id'] = data.temp_id
    await send_message(json_message, chat.members, connections_manager)
