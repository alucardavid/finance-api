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

class IncomingCreate(BaseModel):
    description: str 
    amount: float
    source: str
    date: datetime
    status: str = Field(default= None)

class IncomingUpdate(BaseModel):
    description: str = Field(default= None, min_length=3)
    amount: float = Field(default= None, gt=0)
    source: str = Field(default= None, min_length=3)
    date: datetime = Field(default= None)
    status: str = Field(default= None)