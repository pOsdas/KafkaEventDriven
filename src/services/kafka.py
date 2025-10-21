from confluent_kafka import Producer
import json
from typing import Dict
import logging

from src.config.settings import settings

logger = logging.getLogger(__name__)

KAFKA_CONFIG = {
    "bootstrap.servers": settings.kafka_bootstrap_servers,
    "client.id": settings.kafka_client_id,
    "acks": settings.kafka_acks,
}

producer = Producer(KAFKA_CONFIG)


def delivery_report(err, msg):
    """Callback для логирования доставки сообщения"""
    if err is not None:
        logger.error(f"Доставка провалилась: {err}")
    else:
        logger.info(f"Сообщение отправлено к {msg.topic()} [{msg.partition()}]")


def send_event_to_kafka(event: Dict):
    try:
        data = json.dumps(event).encode("utf-8")
        producer.produce(settings.kafka_topic, value=data, callback=delivery_report)
        producer.flush()
    except Exception as e:
        logger.exception(f"Ошибка при отправке события: {e}")



