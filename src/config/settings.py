from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class RunModel(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8004


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    app: str = "/app"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_pre_ping: bool = True
    max_overflow: int = 10
    pool_size: int = 50

    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "pk": "pk_%(table_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env-template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__"
    )
    # Docker
    docker: bool = False

    # Kafka
    kafka_client_id: str = "event-producer"
    kafka_acks: str = "all"
    kafka_topic: str = "events"

    @computed_field
    @property
    def kafka_bootstrap_servers(self) -> str:
        """при docker-true будет kafka:9092"""
        if self.docker:
            return "kafka:9092"
        return "localhost:9092"

    # ClickHouse (понадобится позже)
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 8123
    clickhouse_database: str = "analytics"

    # Redis (для idempotency)
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Other
    secret_key: str

    run: RunModel = RunModel()
    api: ApiPrefix = ApiPrefix()
    db: DataBaseConfig


settings = Settings()