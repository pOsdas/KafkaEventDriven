import asyncio
import json
from aiokafka import AIOKafkaConsumer

from src.server_logger import logger
from src.config.settings import settings


class BaseConsumer:
    def __init__(self, topic: str, group_id: str):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = settings.kafka_bootstrap_servers
        self.consumer: AIOKafkaConsumer | None = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )

        await self.consumer.start()
        logger.info(f"Consumer '{self.__class__.__name__}' слушает топик '{self.topic}'")

        try:
            async for message in self.consumer:
                await self.process_message(message)
        except asyncio.CancelledError:
            logger.warning(f"Consumer '{self.__class__.__name__}' остановлен вручную")
        except Exception as e:
            logger.exception(f"Ошибка в consumer '{self.__class__.__name__}': {e}")
        finally:
            await self.stop()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"Consumer '{self.__class__.__name__}' остановлен")

    async def process_message(self, message):
        raise NotImplemented("process_message() должен быть переопределён в наследнике")