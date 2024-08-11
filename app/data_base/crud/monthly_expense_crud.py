from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime
from ..schemas import monthly_expense_schema
from ..models import monthly_expense_model

def get_all_expenses(db: Session, skip: int = 0, limit: int = 100, order_by: str = "id asc"):
    """Get all monthly expenses"""
    return db.query(monthly_expense_model.MonthlyExpense).order_by(text(order_by)).offset(skip).limit(limit).all()

def get_expense_by_id(db: Session, expense_id):
    """Get a expense by id"""
    return db.query(monthly_expense_model.MonthlyExpense).get(expense_id)


def create_expense(db: Session, new_expense: monthly_expense_schema.MonthlyExpenseCreate):
    """Create a new expense"""
    db_expense = monthly_expense_model.MonthlyExpense(
        place = new_expense.place,
        description = new_expense.description,
        date = new_expense.date,
        amount = new_expense.amount,
        total_plots = new_expense.total_plots,
        current_plot = new_expense.current_plot,
        due_date = new_expense.due_date,
        status = "Pendente",
        created_at = datetime.now(),
        expense_category_id = new_expense.expense_category_id,
        form_of_payment_id = new_expense.form_of_payment_id,
        user_id = 1
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense

def delete_expense(db: Session, expense_id: int):
    """Delete a expense"""
    db_expense = db.query(monthly_expense_model.MonthlyExpense).get(expense_id)
    if db_expense is not None:
        db.delete(db_expense)
        db.commit()
        return expense_id
    else:
        return None
        
    