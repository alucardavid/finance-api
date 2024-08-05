from datetime import datetime
from pydantic import BaseModel

class Balance(BaseModel):
    id: int
    description: str
    value: float
    created_at: datetime = datetime.now
    updated_at: datetime 
    user_id: int | None = 1
    show: str | None

class BalanceCreate(BaseModel):
    description: str
    value: float
    show: str | None
    