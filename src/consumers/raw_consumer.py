import json
from src.server_logger import logger
from src.consumers.base_consumer import BaseConsumer


class RawConsumer(BaseConsumer):
    async def process_message(self, message):
        try:
            data = json.loads(message.value.decode('utf-8'))
        except json.JSONDecodeError:
            data = message.value.decode()

        logger.info(f"[RawConsumer] Получено сообщение из Kafka: {data}")
