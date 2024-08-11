from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import monthly_expense_model
from ..data_base.schemas import monthly_expense_schema
from ..data_base.crud import monthly_expense_crud
from ..data_base.database import engine, get_db

monthly_expense_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def read_monthly_expenses(response: Response, skip: int = 0, limit: int = 100, order_by: str = "id asc", db: Session = Depends(get_db)):
    """Retrieve all monthly expenses"""
    try:
        monthly_expenses = monthly_expense_crud.get_all_expenses(db, skip, limit, order_by)
        return monthly_expenses
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}

@router.get("/{expense_id}")
def read_monthly_expense_by_id(expense_id: int, response: Response, db: Session = Depends(get_db)):
    """Get a expense by id"""
    expense = monthly_expense_crud.get_expense_by_id(db, expense_id)
    if expense is not None:
        return expense
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.post("/")
def create_monthly_expense(response: Response, new_expense: monthly_expense_schema.MonthlyExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    try:
        return monthly_expense_crud.create_expense(db, new_expense)
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}
    
@router.delete("/{expense_id}")
def delete_monthly_expense(expense_id: int, response: Response, db: Session = Depends(get_db)):
    """Delete a expense"""
    try:
        expense = monthly_expense_crud.delete_expense(db, expense_id)
        if expense is None:
            response.status_code = status.HTTP_404_NOT_FOUND

    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}