from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Event(BaseModel):
    event_id: UUID = Field(default_factory=uuid4())
    user_id: int
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = Field(default_factory=dict)
