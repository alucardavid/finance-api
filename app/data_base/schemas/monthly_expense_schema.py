from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class MonthlyExpense(BaseModel):
    id: int
    place: str
    description: str
    date: datetime
    amount: Decimal
    total_plots: int
    current_plot: int
    due_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    expense_category_id: int
    form_of_payment_id: int
    user_id: int

class MonthlyExpenseCreate(BaseModel):
    place: str = Field(nullable= False, min_length=2)
    description: str = Field(nullable=False, min_length=2)
    date: datetime = Field(nullable=False)
    amount: Decimal = Field(gt=0, nullable=False)
    total_plots: int = Field(default= None)
    current_plot: int = Field(default= None)
    due_date: datetime = Field(nullable=False)
    expense_category_id: int
    form_of_payment_id: int
    