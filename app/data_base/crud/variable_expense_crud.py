from sqlalchemy.orm import Session, joinedload, defaultload
from sqlalchemy.sql import text
from typing import List
from datetime import datetime
from ..schemas import variable_expense_schema as schema
from ..models import variable_expense_model as model
from ..models import form_of_payment_model 

def get_all_expenses(db: Session, skip: int = 0, limit: int = 100, order_by: str = "id asc"):
    """Get all variable expenses"""
    return db.query(model.VariableExpense).options(joinedload(model.VariableExpense.form_of_payments).joinedload(form_of_payment_model.FormOfPayment.balances)).order_by(text(order_by)).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    """Get expense by id"""
    return db.query(model.VariableExpense).options(joinedload(model.VariableExpense.form_of_payments).joinedload(form_of_payment_model.FormOfPayment.balances)).get(expense_id)

def add_expense(db: Session, new_expense: schema.VariableExpenseCreate):
    """Create a new expense"""
    db_expense = model.VariableExpense(
        description = new_expense.description,
        type = new_expense.type,
        amount = new_expense.amount,
        date = new_expense.date,
        created_at = datetime.now(),
        form_of_payment_id = new_expense.form_of_payment_id,
        place = new_expense.place,
        user_id = 1
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    if new_expense.type == "Despesa":
        db_expense.form_of_payments.balances.value -= new_expense.amount
        db_expense.form_of_payments.balances.updated_at = datetime.now()
    else:
        db_expense.form_of_payments.balances.value += new_expense.amount
        db_expense.form_of_payments.balances.updated_at = datetime.now()

    db.commit()
    db.refresh(db_expense)
    
    return(db_expense)

def delete_expense(db: Session, expense_id: int):
    """Delete a expense"""
    db_expense = db.query(model.VariableExpense).get(expense_id)

    if db_expense is not None:
        db.delete(db_expense)
        db.commit()
        return expense_id
    else:
        return None