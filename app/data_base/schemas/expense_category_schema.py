from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class ExpenseCategory(BaseModel):
    id: int
    description: str
    show: str
    created_at: datetime
    updated_at: datetime

class ExpenseCategoryCreate(BaseModel):
    description: str
    show: str

class ExpenseCategoryUpdate(BaseModel):
    description: str = Field(default= None, min_length=3)
    show: str = Field(default= None, min_length=1, max_length=1)