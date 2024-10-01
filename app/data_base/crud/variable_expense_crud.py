from sqlalchemy.orm import Session, joinedload, defaultload
from sqlalchemy.sql import text, func, or_, and_
from typing import List
from datetime import datetime
from ..schemas import variable_expense_schema as schema
from ..models import variable_expense_model as model
from ..models import form_of_payment_model 

def get_all_expenses(db: Session, page: int = 1, limit: int = 100, order_by: str = "id asc", where: str = None):
    """Get all variable expenses"""

    if where is None:
        items = (db.query(model.VariableExpense)
                .options(joinedload(model.VariableExpense.form_of_payments)
                        .joinedload(form_of_payment_model.FormOfPayment.balances))
                .order_by(text(order_by))
                .offset((page * limit) - limit)
                .limit(limit).all())
        
        count = (db.query(model.VariableExpense).count())
    else:
        items = (db.query(model.VariableExpense)
                .join(form_of_payment_model.FormOfPayment)
                .options(joinedload(model.VariableExpense.form_of_payments)
                        .joinedload(form_of_payment_model.FormOfPayment.balances))
                .where(or_(
                    model.VariableExpense.place.like(f"%{where}%"),
                    model.VariableExpense.description.like(f"%{where}%"),
                    model.VariableExpense.type.like(f"%{where}%"),
                    func.to_char(model.VariableExpense.date, "dd/MM/yyyy").like(f"%{where}%"),
                    func.replace(func.replace(func.replace(func.to_char(model.VariableExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    form_of_payment_model.FormOfPayment.description.like(f"%{where}%")
                ))
                .order_by(text(order_by))
                .offset((page * limit) - limit)
                .limit(limit).all())
        
        count = (db.query(model.VariableExpense)
                .join(form_of_payment_model.FormOfPayment)
                .options(joinedload(model.VariableExpense.form_of_payments)
                        .joinedload(form_of_payment_model.FormOfPayment.balances))
                .where(or_(
                    model.VariableExpense.place.like(f"%{where}%"),
                    model.VariableExpense.description.like(f"%{where}%"),
                    model.VariableExpense.type.like(f"%{where}%"),
                    func.to_char(model.VariableExpense.date, "dd/MM/yyyy").like(f"%{where}%"),
                    func.replace(func.replace(func.replace(func.to_char(model.VariableExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    form_of_payment_model.FormOfPayment.description.like(f"%{where}%")
                )).count())
        
    result = {
        'count': count,
        'total_pages': int((count/ limit)+1),
        'limit': limit,
        'page': page,
        'items': items
    }

    return result

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
    
def update_expense(db: Session, expense_id: int, new_expense: schema.VariableExpenseCreate):
    """update a expense"""
    db_expense = db.query(model.VariableExpense).get(expense_id)
    if db_expense is not None:
        db_expense.place = new_expense.place
        db_expense.description = new_expense.description
        db_expense.date = new_expense.date
        db_expense.type = new_expense.type
        db_expense.amount = new_expense.amount
        db_expense.form_of_payment_id = new_expense.form_of_payment_id
        db_expense.updated_at = datetime.now()
        db.commit()
        db.refresh(db_expense)

    return db_expense