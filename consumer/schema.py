from pydantic import BaseModel
from pydantic import Field


class PingHost(BaseModel):
    host: str = Field(description="Host")


class Restore(BaseModel):
    monitor_id: int = Field()
