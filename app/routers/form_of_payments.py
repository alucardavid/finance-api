from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import form_of_payment_model, balance_model
from ..data_base.schemas import form_of_payment_schema
from ..data_base.crud import form_of_payment_crud
from ..data_base.database import engine, get_db
from typing import List, Optional

form_of_payment_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def read_form_of_payments(response: Response, skip: int = 0, limit: int = 0, order_by: str = "id asc", db: Session = Depends(get_db)):
    """Retrieve all form of payments"""
    # try:
    form_of_payments = form_of_payment_crud.get_all_form_of_payments(db, skip, limit, order_by)
    
    return form_of_payments
    # except Exception as e:
    #     response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    #     return { "error_message": e}