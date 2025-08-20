from asyncio.log import logger
from sqlalchemy.orm import Session, joinedload, defaultload
from sqlalchemy.sql import text, func, or_, and_
from typing import List
from datetime import datetime
from ..schemas import variable_expense_schema as schema
from ..models import variable_expense_model as model
from ..models import form_of_payment_model 

def get_all_expenses(db: Session, page: int = 1, limit: int = 100, order_by: str = "id asc", where: str = None, balance_id: int = None) -> dict:
    """Get all variable expenses"""

    filters = []
    all_filters = []

    if where:
        filters.append(model.VariableExpense.place.like(f"%{where}%"))
        filters.append(model.VariableExpense.description.like(f"%{where}%"))
        filters.append(model.VariableExpense.type.like(f"%{where}%"))
        filters.append(func.to_char(model.VariableExpense.date, "dd/MM/yyyy").like(f"%{where}%"))
        filters.append(func.replace(func.replace(func.replace(func.to_char(model.VariableExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"))
        filters.append(form_of_payment_model.FormOfPayment.description.like(f"%{where}%"))

    # Create the query with joinedload to eagerly load related FormOfPayment and Balance
    query = db.query(model.VariableExpense).join(form_of_payment_model.FormOfPayment).options(
        joinedload(model.VariableExpense.form_of_payments).joinedload(form_of_payment_model.FormOfPayment.balance)
    ) 

    # If there are filters, apply them
    if where:
        all_filters.append(or_(*filters))

    # If balance_id is provided, filter by balance_id    
    if balance_id:
        all_filters.append(and_(form_of_payment_model.FormOfPayment.balance_id == balance_id))

    if all_filters:
        query = query.filter(*all_filters)
    
    count_query = query

    # Validate order_by input
    if order_by.strip().lower() == "desc" or order_by.strip().lower() == "asc":
        order_by = "variable_expenses.id desc"  # Default safe value
    elif not order_by:
        order_by = "variable_expenses.id asc"  # Default safe value

    items = query.order_by(text(order_by)).offset((page * limit) - limit).limit(limit).all()
    count = count_query.count()
    
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
    return db.query(model.VariableExpense).options(joinedload(model.VariableExpense.form_of_payments).joinedload(form_of_payment_model.FormOfPayment.balance)).get(expense_id)

def add_expense(db: Session, new_expense: schema.VariableExpenseCreate, update_balance=False):
    """Create a new expense"""
    if _expense_exists(db, new_expense):
       logger.warning(f"Expense already exists: {new_expense.id_transaction}")
       return

    db_expense = model.VariableExpense(
        description = new_expense.description,
        type = new_expense.type,
        amount = new_expense.amount,
        date = new_expense.date,
        created_at = datetime.now(),
        form_of_payment_id = new_expense.form_of_payment_id,
        place = new_expense.place,
        user_id = 1,
        id_transaction = new_expense.id_transaction
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    # Update the balance if necessary
    if update_balance:
        if new_expense.type == "Despesa":
            db_expense.form_of_payments.balance.value -= new_expense.amount
            db_expense.form_of_payments.balance.updated_at = datetime.now()
        else:
            db_expense.form_of_payments.balance.value += new_expense.amount
            db_expense.form_of_payments.balance.updated_at = datetime.now()

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
        db_expense.id_transaction = new_expense.id_transaction  
        db.commit()
        db.refresh(db_expense)

    return db_expense

def get_all_places(db: Session, where: str):
    """Get all places"""
    items = []

    db_places = (
        db.query(model.VariableExpense.place)
        .where(func.lower(model.VariableExpense.place).like(f"{where.lower()}%"))
        .group_by(model.VariableExpense.place)
        .order_by(model.VariableExpense.place)
        .all()
    )
    
    count = (
        db.query(model.VariableExpense.place)
        .where(func.lower(model.VariableExpense.place).like(f"{where.lower()}%"))
        .group_by(model.VariableExpense.place)
        .count()
    )

    for place in db_places:
        items.append(place[0])

    places = {
        "total": count,
        "items": items
    }

    return places

def get_all_descriptions(db: Session, where: str):
    """Get all descriptions"""
    items = []

    db_descriptions = (
        db.query(model.VariableExpense.description)
        .where(func.lower(model.VariableExpense.description).like(f"{where.lower()}%"))
        .group_by(model.VariableExpense.description)
        .order_by(model.VariableExpense.description)
        .all()
    )
    
    count = (
        db.query(model.VariableExpense.description)
        .where(func.lower(model.VariableExpense.description).like(f"{where.lower()}%"))
        .group_by(model.VariableExpense.description)
        .count()
    )

    for description in db_descriptions:
        items.append(description[0])

    descriptions = {
        "total": count,
        "items": items
    }

    return descriptions

def _expense_exists(db: Session, expense: schema.VariableExpenseCreate) -> bool:
    return db.query(model.VariableExpense).filter_by(
        id_transaction=expense.id_transaction,
    ).first() is not None