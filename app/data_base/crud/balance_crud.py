from fastapi.logger import logger
from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas import balance_schema
from ..models import balance_model
from sqlalchemy.sql import text


def get_balances(db: Session, skip: int = 0, limit: int = 100, order_by: str = "id asc"):
    """Get all balances"""
    return db.query(balance_model.Balance).order_by(text(order_by)).offset(skip).limit(limit).all()

def get_balance_by_id(db: Session, balance_id: int):
    """Get a balance by Id"""
    balance = db.query(balance_model.Balance).get(balance_id)
    return balance

def create_balance(db: Session, balance: balance_schema.BalanceCreate):
    """Create a new balance"""
    db_balance = balance_model.Balance(
        description= balance.description,
        value= balance.value,
        created_at= datetime.now(),
        user_id=1,
        show=balance.show
    )

    db.add(db_balance)
    db.commit()
    db.refresh(db_balance)

    return db_balance

def delete_balance(db: Session, balance_id):
    """Delete a balance by id"""
    db_balance = db.query(balance_model.Balance).get(balance_id)
    if db_balance is not None:
        db.delete(db_balance)
        db.commit()
        return balance_id
    else:
        return None
    
def update_balance(db: Session, balance_id: int, new_balance: balance_schema.BalanceUpdate):
    """Update a balance by id"""
    db_balance = db.query(balance_model.Balance).get(balance_id)
    if db_balance is not None:
        fields = ["description", "value", "show", "status_open_finance", "id_item", "id_account_bank"]
        for field in fields:
            new_value = getattr(new_balance, field, None)
            if new_value is not None:
                setattr(db_balance, field, new_value)

        
        db_balance.updated_at = datetime.now()
        db.commit()
        db.refresh(db_balance)
        logger.info(f"Balance {balance_id} updated successfully. New values: {new_balance}")
        return db_balance
    else:
        return None

def increase_balance(db: Session, balance_id: int, new_value: balance_schema.BalanceIncrease):
    """Increase the balance value"""
    db_balance = db.query(balance_model.Balance).get(balance_id)
    if db_balance is not None:
        db_balance.value += new_value.value
        db_balance.updated_at = datetime.now()
        db.commit()
        db.refresh(db_balance)

    return db_balance
    
def decrease_balance(db: Session, balance_id: int, new_value: balance_schema.BalanceDecrease):
    """Decrease the balance value"""
    db_balance = db.query(balance_model.Balance).get(balance_id)
    if db_balance is not None:
        db_balance.value -= new_value.value
        db_balance.updated_at = datetime.now()
        db.commit()
        db.refresh(db_balance)

    return db_balance
    

