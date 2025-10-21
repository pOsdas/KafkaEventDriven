from fastapi import APIRouter

from src.config.settings import settings

api_v1_router = APIRouter(
    prefix=settings.api.v1.prefix,
)