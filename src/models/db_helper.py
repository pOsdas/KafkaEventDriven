from typing import AsyncGenerator
import logging
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession
)

from src.config.settings import settings
from src.server_logger import logger


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_pre_ping: bool = True,
            max_overflow: int = 10,
            pool_size: int = 5,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_pre_ping=pool_pre_ping,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        try:
            await self.engine.dispose()
            logger.info("DB engine disposed")
        except Exception as e:
            logger.exception("Error disposing DB engine: %s", e)

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    @staticmethod
    def create_db_if_not_exists():
        import psycopg2
        from urllib.parse import urlparse

        parsed = urlparse(str(settings.db.url))
        target_db = parsed.path.lstrip("/")
        user = parsed.username
        password = parsed.password
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432

        conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
            exists = cur.fetchone()
            if not exists:
                logger.info(f"База данных '{target_db}' не найдена. Создаю...")
                cur.execute(f"CREATE DATABASE {target_db}")
            else:
                logger.info(f"База данных '{target_db}' уже существует.")
        finally:
            cur.close()
            conn.close()


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_pre_ping=settings.db.pool_pre_ping,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)