from clickhouse_driver import Client
from src.server_logger import logger
from src.config.settings import settings


class ClickHouseClient:
    def __init__(self):
        self.client = Client(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            user=settings.clickhouse.user,
            password=settings.clickhouse.password,
            database=settings.clickhouse.database
        )
        self._init_table()

    def _init_table(self):
        self.client.execute("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                event_id String,
                event_type String,
                payload String,
                created_at DateTime DEFAULT now()
            )
            ENGINE = MergeTree()
            ORDER BY created_at
        """)
        logger.info("[ClickHouse] Таблица analytics_events готова")

    def insert_event(self, event_id: str, event_type: str, payload: str):
        self.client.execute(
            "INSERT INTO analytics_events (event_id, event_type, payload) VALUES",
            [(event_id, event_type, payload)]
        )
        logger.info(f"[ClickHouse] Событие {event_id} сохранено")

    def get_recent_events(self, limit: int = 10):
        rows = self.client.execute(f"SELECT * FROM analytics_events ORDER BY created_at DESC LIMIT {limit}")
        return rows


clickhouse = ClickHouseClient()