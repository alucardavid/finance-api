from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text, func
from typing import List
from datetime import datetime
from ..schemas import monthly_expense_schema
from ..models import monthly_expense_model as model
from ..models import form_of_payment_model
import sys

def get_all_expenses(db: Session, page: int = 1, limit: int = 100, order_by: str = "id asc", due_date: str = None):
    """Get all monthly expenses"""
        
    if due_date is None:
        items = (db.query(model.MonthlyExpense)
               .options(joinedload(model.MonthlyExpense.form_of_payments)
               .joinedload(form_of_payment_model.FormOfPayment.balances))
               .order_by(text(order_by))
               .offset((page * limit) - limit)
               .limit(limit).all())

        count = db.query(model.MonthlyExpense).count()

    else:
        items = (db.query(model.MonthlyExpense)
               .where(func.to_char(model.MonthlyExpense.due_date, "YYYY-MM") == due_date)
               .options(joinedload(model.MonthlyExpense.form_of_payments)
               .joinedload(form_of_payment_model.FormOfPayment.balances))
               .order_by(text(order_by))
               .offset((page * limit) - limit)
               .limit(limit).all())
        
        count = (db.query(model.MonthlyExpense)
               .where(func.to_char(model.MonthlyExpense.due_date, "YYYY-MM") == due_date)
               .count())
    
    result = {
        'count': count,
        'total_pages': int((count/ limit)+1),
        'limit': limit,
        'page': page,
        'items': items
    }

    return result

def get_expense_by_id(db: Session, expense_id):
    """Get a expense by id"""
    return db.query(model.MonthlyExpense).options(joinedload(model.MonthlyExpense.form_of_payments).joinedload(form_of_payment_model.FormOfPayment.balances)).get(expense_id)

def create_expense(db: Session, new_expense: monthly_expense_schema.MonthlyExpenseCreate):
    """Create a new expense"""
    db_expense = model.MonthlyExpense(
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
    db_expense = db.query(model.MonthlyExpense).get(expense_id)
    if db_expense is not None:
        db.delete(db_expense)
        db.commit()
        return expense_id
    else:
        return None
        
def update_expense(db: Session, expense_id: int, new_expense: monthly_expense_schema.MonthlyExpenseUpdate):
    """Update a expense"""
    db_expense = db.query(model.MonthlyExpense).get(expense_id)

    if db_expense is not None:
        if new_expense.place is not None:
            db_expense.place = new_expense.place
        
        if new_expense.description is not None:
            db_expense.description = new_expense.description

        if new_expense.date is not None:
            db_expense.date = new_expense.date

        if new_expense.amount is not None:
            db_expense.amount = new_expense.amount
        
        if new_expense.total_plots is not None:
            db_expense.total_plots = new_expense.total_plots
        
        if new_expense.current_plot is not None:
            db_expense.current_plot = new_expense.current_plot

        if new_expense.due_date is not None:
            db_expense.due_date = new_expense.due_date
        
        if new_expense.expense_category_id is not None:
            db_expense.expense_category_id = new_expense.expense_category_id

        if new_expense.form_of_payment_id is not None:
            db_expense.form_of_payment_id = new_expense.form_of_payment_id

        db_expense.updated_at = datetime.now()
        db.commit()
        db.refresh(db_expense)

    return db_expense
   
def pay_expense(db: Session, expense_id: int):
    """Change expense status to Pago"""
    db_expense = db.query(model.MonthlyExpense).get(expense_id)

    if db_expense is not None:
        db_expense.status = "Pago"
        db.commit()
        db.refresh(db_expense)
        
    return db_expense

def pay_expenses(db: Session, expenses_id: monthly_expense_schema.MonthlyExpensesPay):
    """Pay all expenses in the list"""
    if expenses_id is not None:
        db.query(model.MonthlyExpense).filter(model.MonthlyExpense.id.in_(expenses_id)).update({"status": "Pago"})
        db.commit()
        
        db_expenses_paid = db.query(model.MonthlyExpense).filter(model.MonthlyExpense.id.in_(expenses_id)).all()
        
    return db_expenses_paid

    


        
    