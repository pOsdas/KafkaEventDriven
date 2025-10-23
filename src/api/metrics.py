from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from src.server_logger import logger

router = APIRouter(tags=["Metrics"])


@router.get("/metrics")
async def metrics():
    try:
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        logger.error(f"Ошибка при генерации метрик: {e}")
        return Response(status_code=500, content=str(e))