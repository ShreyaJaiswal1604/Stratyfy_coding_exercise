from pydantic import BaseModel
from typing import Optional

# Base schema for Sundae
class SundaeBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

# Extended schema for GET /sundaes/{id}
class SundaeWithMetrics(SundaeBase):
    volume: int
    revenue: float

    class Config:
        orm_mode = True
