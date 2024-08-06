from datetime import datetime
from pydantic import BaseModel, Field

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
    show: str 

class BalanceUpdate(BaseModel):
    description: str = Field(default= None, min_length=5)
    value: float = Field(default= None)
    show: str = Field(default= None, min_length=1, max_length=1)

    