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

    def insert_event(self, table: str, data: dict):
        try:
            columns = ", ".join(data.keys())
            values = tuple(data.values())
            self.client.execute(
                f"INSERT INTO {table} ({columns}) VALUES", [values]
            )
            logger.info(f"Записано событие в ClickHouse ({table}): {data}")
        except Exception as e:
            logger.error(f"Ошибка записи в ClickHouse: {e}")


clickhouse = ClickHouseClient()