import motor.motor_asyncio

from core.settings import get_settings

settings = get_settings()

MONGO_DETAILS = (
    "mongodb://"
    f"{settings.mongo.user}:{settings.mongo.password}"
    f"@{settings.mongo.host}:{settings.mongo.port}"
)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.chat_app
