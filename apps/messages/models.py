from datetime import datetime
from typing import List, Optional, Union

from bson.objectid import ObjectId
from pydantic import BaseConfig, BaseModel, Field

from core.models import PydanticObjectId


class Message(BaseModel):
    id: Union[PydanticObjectId, str] = Field(alias="_id", default=None)

    sender: int
    chat_id: PydanticObjectId
    created_at: datetime
    is_read: bool

    text: Optional[str]

    class Meta:
        extra = "allow"

    class Config(BaseConfig):
        orm_mode = True
        json_encoders = {PydanticObjectId: str, ObjectId: str}


class MessagesHistory(BaseModel):
    total: int
    messages: List[Message]

    class Config:
        orm_mode = True
        json_encoders = {PydanticObjectId: str, ObjectId: str}


class MessageRequest(BaseModel):
    text: str
    user_id: Optional[int]
    chat_id: PydanticObjectId
    temp_id: Optional[str]


class MessageAction(BaseModel):
    action: str = "new_message"
    data: Message

    class Config:
        json_encoders = {PydanticObjectId: str, ObjectId: str}
