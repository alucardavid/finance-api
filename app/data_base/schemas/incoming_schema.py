from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class Incoming(BaseModel):
    id: int
    description: str
    amount: float
    source: str
    date: datetime
    created_at: datetime
    updated_at: datetime
    status: str

    class Config:
        from_attributes = True

