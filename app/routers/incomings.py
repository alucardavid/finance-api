from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import incoming_model as model
from ..data_base.crud import incoming_crud as crud
from ..data_base.database import SessionLocal, engine, get_db

model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/", status_code=201)
def read_incomings(status: str = "Pendente", order_by: str = "id asc", db: Session = Depends(get_db)):
    """Retrieve all incomings"""

    incomings = crud.get_incomings(db, status, order_by)

    return incomings