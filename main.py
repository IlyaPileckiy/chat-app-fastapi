from fastapi import FastAPI, APIRouter

from core.endpoints import router as main_router
from core.postgres_client import database
from core.settings import get_settings

settings = get_settings()


app = FastAPI(title="chat")


@app.on_event("startup")
async def on_startup() -> None:
    await database.create_pool()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await database.close_pool()


api_router = APIRouter()

app.include_router(main_router, prefix="", tags=["Chat router"])
