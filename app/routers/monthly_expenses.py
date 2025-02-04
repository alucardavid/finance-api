from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..data_base.models import monthly_expense_model
from ..data_base.schemas import monthly_expense_schema
from ..data_base.crud import monthly_expense_crud as crud
from ..data_base.database import engine, get_db
from typing import List, Optional
import json

monthly_expense_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def read_monthly_expenses(response: Response, page: int = 1, limit: int = 50, 
                          order_by: str = "monthly_expenses.id desc", due_date: str = None, 
                          where: str = None, type_return: str = "standard", status: str = None, db: Session = Depends(get_db)):
    """Retrieve all monthly expenses"""
    try:
        match type_return:
            case "standard":
                monthly_expenses = crud.get_all_expenses(db, page, limit, order_by, due_date, where)
            case "grouped_by_month":
                monthly_expenses = crud.get_expenses_grouped_by_month(db, where)
            case "grouped_by_category":
                monthly_expenses = crud.get_expenses_grouped_by_category(db, due_date)
            case "grouped_by_place":
                monthly_expenses = crud.get_expenses_grouped_by_place(db, due_date, status)

        return monthly_expenses
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        raise

@router.get("/{expense_id}")
def read_monthly_expense_by_id(expense_id: int, response: Response, db: Session = Depends(get_db)):
    """Get a expense by id"""
    expense = crud.get_expense_by_id(db, expense_id)
    if expense is not None:
        return expense
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.post("/")
async def create_monthly_expense(response: Response, new_expense: monthly_expense_schema.MonthlyExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    expenses = []
    try:
        if not crud.expense_exist(db, new_expense):
            if new_expense.total_plots > 1:
                db_expense = crud.expense_not_exist_check_amount(db, new_expense)
                if db_expense is not None:
                    expense = crud.update_expense(db, db_expense.id, monthly_expense_schema.MonthlyExpenseUpdate(amount=new_expense.amount))
                    return expense
                else:
                    expenses =  await crud.create_expense(db, new_expense)
                    return expenses
            else:
                expenses =  await crud.create_expense(db, new_expense)
                return expenses
        else:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return { "error_message": "Expense already exists" }
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        raise
        
    
@router.delete("/{expense_id}")
def delete_monthly_expense(expense_id: int, response: Response, db: Session = Depends(get_db)):
    """Delete a expense"""
    try:
        expense = crud.delete_expense(db, expense_id)
        if expense is None:
            response.status_code = status.HTTP_404_NOT_FOUND

    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}
    
@router.put("/{expense_id}")
def update_monthly_expense(expense_id: int, response: Response, new_expense: monthly_expense_schema.MonthlyExpenseUpdate, db: Session = Depends(get_db)):
    """Update a expense"""
    try:
        expense = crud.update_expense(db, expense_id, new_expense)
        if expense is not None:
            return expense
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}

@router.put("/pay/{expense_id}")
def pay_monthly_expense(expense_id: int, response: Response, db: Session = Depends(get_db)):
    """Pay a monthly expense change de staus to Pago"""
    try:
        expense = crud.pay_expense(db, expense_id)
        if expense is not None:
            return expense
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}
    
@router.put("/pay/")
def pay_monthly_expenses(expenses_id: List[int], response: Response, db: Session = Depends(get_db)):
    """Pay all expenses in the list"""
    try:
        expenses_paid = crud.pay_expenses(db, expenses_id)
        if expenses_paid is not None:
            return expenses_paid  
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}
    
@router.get("/descriptions/")
def read_all_descriptions(where: str, response: Response, db: Session = Depends(get_db)):
    """Get all descriptions withou repetitions"""

    return crud.get_all_descriptions(db, where)
