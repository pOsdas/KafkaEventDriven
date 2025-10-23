from fastapi import (
    APIRouter, HTTPException
)
import logging
from src.models import Event
from src.services.kafka import send_event_to_kafka

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/app", tags=["APP"])


@router.post("/event")
async def produce_event(event: Event):
    try:
        logger.info(f"Received event: {event.json()}")
        send_event_to_kafka(event)
        return {"status": "ok", "message": "Event отправлен в kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))