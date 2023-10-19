
import logging
import time

from fastapi import (
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    Header
)

from apps.chats.models import Chat, ChatRequest, ChatsHistory
from apps.chats.repository import ChatRepository
from apps.messages.models import MessagesHistory
from apps.messages.repository import MessageRepository
from apps.messages.services import process_new_message
from core.connections_manager import ConnectionManager
from core.deps import get_db
from core.models import PydanticObjectId
from core.postgres_client import Database


connections_manager = ConnectionManager()
router = APIRouter()

wb_logger = logging.getLogger("uvicorn")


@router.get("/chat/history/{chat_id}/")
async def history(
    request: Request, chat_id: PydanticObjectId, offset: int, limit: int
) -> MessagesHistory:
    history = await MessageRepository.get_chat_history(
        chat_id=chat_id, offset=offset, limit=limit
    )
    return history


@router.post("/chat/create/")
async def create_chat(
    request: Request, data: ChatRequest, db: Database = Depends(get_db)
) -> Chat:
    return await ChatRepository.get_chat_by_memebers(
        db=db,
        sender_id=int(request.state.user_id),
        members=sorted([int(request.state.user_id), *data.members]),
    )


@router.get("/chat/list/")
async def users_chats(
    request: Request, offset: int, limit: int, db: Database = Depends(get_db)
) -> ChatsHistory:
    return await ChatRepository.get_users_chats(
        db, int(request.state.user_id), offset=offset, limit=limit
    )


@router.websocket("/chat/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int = Header(alias="X-user"),
):
    wb_logger.warning(f"Try connect: {websocket.headers}")
    try:
        await connections_manager.connect(websocket, user_id)
        while True:
            start_time = time.time()
            wb_logger.warning(f"{user_id} <-- connected")
            data = await websocket.receive_json()
            action = data.get('action')
            if action == "new_message":
                await process_new_message(
                    data['data'],
                    user_id,
                    connections_manager,
                )
                wb_logger.warning(f"Time: {time.time() - start_time} ({data})")

            else:
                await websocket.send_json(
                    {"error": "Action does not exist"}
                )

    except WebSocketDisconnect as error:
        wb_logger.warning(f"{user_id} <-- disconnect code {error}")
        await connections_manager.disconnect(user_id)
