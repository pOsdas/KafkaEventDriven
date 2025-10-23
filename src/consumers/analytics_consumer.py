import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.services.metrics import events_processed_total, events_failed_total
from src.models import AnalyticsEvent
from src.models.db_helper import db_helper
from src.consumers.base_consumer import BaseConsumer
from src.server_logger import logger


class AnalyticsConsumer(BaseConsumer):
    async def process_message(self, message):
        try:
            data = json.loads(message.value.decode('utf-8'))
            event_type = data.get("event_type", "unknown")

            async with db_helper.session_factory as session:
                await self.save_event(session, event_type, data)
                await session.commit()

            events_processed_total.labels(consumer="analytics_consumer").inc()
            logger.info(f"[AnalyticsConsumer] Событие сохранено в БД: {data}")

        except Exception as e:
            events_failed_total.labels(consumer="analytics_consumer").inc()
            logger.error(f"Ошибка при обработке аналитики: {e}")
            return

    @staticmethod
    async def save_event(session: AsyncSession, event_id: str, event_type: str, data: dict) -> None:
        exists = await session.execute(
            select(AnalyticsEvent).where(AnalyticsEvent.event_id == int(event_id))
        )
        if exists.scalar():
            logger.warning(f"Событие {event_id} уже сохранено, пропускаю")
            return

        event = AnalyticsEvent(
            event_type=event_type,
            payload=data,
        )
        session.add(event)
