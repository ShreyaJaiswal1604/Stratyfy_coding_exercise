from pydantic import BaseModel
from typing import List, Optional

class SundaeBase(BaseModel):
    id: str
    name: str
    description: str

class SundaeResponse(SundaeBase):
    """Schema for GET /sundaes/{id} with volume and revenue."""
    volume: int
    revenue: float

class SundaeListResponse(SundaeBase):
    """Schema for listing all sundaes."""
    pass

class SaleBase(BaseModel):
    sundae_id: str
    timestamp: float
    quantity: int
