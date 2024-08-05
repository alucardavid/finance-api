from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas import balance_schema
from ..models import balance_model

def get_balances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(balance_model.Balance).offset(skip).limit(limit).all()

def create_balance(db: Session, balance: balance_schema.BalanceCreate):
    print(datetime.now)
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
