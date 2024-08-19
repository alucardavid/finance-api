from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List
from .form_of_payment_schema import FormOfPayment


class VariableExpense(BaseModel):
    id: int
    place: str
    description: str
    date: datetime
    type: str
    amount: Decimal
    created_at: datetime
    updated_at: datetime
    user_id: int

    form_of_payments: list[FormOfPayment] = []

    class Config:
        from_attributes = True

class VariableExpenseCreate(BaseModel):
    place: str = Field(nullable= False, min_length=2)
    description: str = Field(nullable=False, min_length=2)
    date: datetime = Field(nullable=False)
    type: str = Field(nullable=False)
    amount: Decimal = Field(gt=0, nullable=False)
    form_of_payment_id: int
