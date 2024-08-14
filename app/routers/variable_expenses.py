from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import variable_expense_model 
from ..data_base.schemas import variable_expense_schema as schema
from ..data_base.crud import variable_expense_crud as crud
from ..data_base.database import engine, get_db
from typing import List, Optional

variable_expense_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def read_variable_expenses(response: Response, skip: int = 0, limit: int = 0, order_by: str = "id asc", db: Session = Depends(get_db)):
    """Retrieve all variable expenses"""
    # try:
    expenses = crud.get_all_expenses(db, skip, limit, order_by)
    return expenses
    # except Exception as e:
    #     response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    #     return { "error_message": e}

@router.post("/")
def add_variable_expense(response: Response, new_expense: schema.VariableExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    expense = crud.add_expense(db, new_expense)
    return expense