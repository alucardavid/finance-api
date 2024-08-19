
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List
from .balance_schema import Balance


class FormOfPayment(BaseModel):
    id: int
    description: str
    created_at: datetime
    updated_at: datetime
    balances: list[Balance] = []

    class Config:
        from_attributes = True

    

class FormOfPaymentCreate(BaseModel):
    description: str = Field(nullable=False, min_length=2)
    balance_id: int