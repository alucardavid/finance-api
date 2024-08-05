from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..data_base.models import balance_model
from ..data_base.crud import balance_crud
from ..data_base.schemas import balance_schema
from ..data_base.database import SessionLocal, engine

balance_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", status_code=201)
def read_balances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve balances"""
    balances = balance_crud.get_balances(db, skip=skip, limit=limit)
    return balances

@router.post("/")
def create_balace(balance: balance_schema.BalanceCreate, db: Session = Depends(get_db)):
    return balance_crud.create_balance(db=db, balance=balance)
