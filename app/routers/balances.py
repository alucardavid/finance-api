from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import balance_model
from ..data_base.crud import balance_crud
from ..data_base.schemas import balance_schema
from ..data_base.database import SessionLocal, engine, get_db

balance_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/", status_code=201)
def read_balances(skip: int = 0, limit: int = 100, order_by: str = "id asc", db: Session = Depends(get_db)):
    """Retrieve balances"""
    balances = balance_crud.get_balances(db, skip, limit, order_by)
    return balances

@router.get("/{balance_id}")
def read_balance_by_id(balance_id, response: Response, db: Session = Depends(get_db)):
    """Retrieve balance by id"""
    balance = balance_crud.get_balance_by_id(db, balance_id)
    if balance == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
    else:
        return balance

@router.post("/")
def create_balace(balance: balance_schema.BalanceCreate, db: Session = Depends(get_db)):
    """Create new balance"""
    return balance_crud.create_balance(db=db, balance=balance)

@router.delete("/{balance_id}")
def delete_balance(balance_id, response: Response, db: Session = Depends(get_db)):
    """Delete a balance"""
    balance = balance_crud.delete_balance(db, balance_id)
    if balance is not None:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.put("/{balance_id}")
def update_balance(balance_id, response: Response, new_balance: balance_schema.BalanceUpdate, db: Session = Depends(get_db)):
    """Update a balance with new values"""
    return balance_crud.update_balance(db, balance_id, new_balance)

@router.post("/increase/{balance_id}")
def increase_balance(balance_id, response: Response, new_value: balance_schema.BalanceIncrease, db: Session = Depends(get_db)):
    """Increase the balance value"""
    balance = balance_crud.increase_balance(db, balance_id, new_value)
    if balance is not None:
        return balance
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.post("/decrease/{balance_id}")
def decrease_balance(balance_id, response: Response, new_value: balance_schema.BalanceDecrease, db: Session = Depends(get_db)):
    """Decrease the balance value"""
    balance = balance_crud.decrease_balance(db, balance_id, new_value)
    if balance is not None:
        return balance
    else:
        response.status_code = status.HTTP_404_NOT_FOUND