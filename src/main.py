import uvicorn
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.models.db_helper import db_helper, DatabaseHelper
from src.models import Base
from src.api.producer import router as event_router
from src.api.metrics import router as metric_router
from src.consumers import RawConsumer
from src.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, DatabaseHelper.create_db_if_not_exists)

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    consumer_task = asyncio.create_task(RawConsumer(topic="events", group_id="api_consumer").start())
    yield
    consumer_task.cancel()
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    title="KafkaEventDriven",
    lifespan=lifespan,
)

app.include_router(event_router)
app.include_router(metric_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello, World!"
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
