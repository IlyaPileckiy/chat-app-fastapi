from datetime import datetime
from typing import Dict, List, Optional

from bson.objectid import ObjectId
from pydantic import BaseConfig, BaseModel, Field

from core.models import PydanticObjectId


class LastMessage(BaseModel):
    date: datetime
    text: str


class Chat(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    members: List[int]
    block: Dict[int, bool] | None
    last_message: Optional[LastMessage]
    name: Optional[str]

    class Config(BaseConfig):
        json_encoders = {ObjectId: str}


class HistoryChats(BaseModel):
    total: int
    chats: List[Chat]

    class Config:
        orm_mode = True
        json_encoders = {PydanticObjectId: str, ObjectId: str}


class ChatRequest(BaseModel):
    members: List[int]
