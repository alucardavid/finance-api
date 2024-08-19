from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import form_of_payment_model, balance_model
from ..data_base.schemas import form_of_payment_schema as schema
from ..data_base.crud import form_of_payment_crud as crud
from ..data_base.database import engine, get_db
from typing import List, Optional

form_of_payment_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def read_form_of_payments(response: Response, skip: int = 0, limit: int = 0, order_by: str = "id asc", db: Session = Depends(get_db)):
    """Retrieve all form of payments"""
    try:
        form_of_payments = crud.get_all_form_of_payments(db, skip, limit, order_by)
    
        return form_of_payments
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}

@router.get("/{form_of_payment_id}")
def get_form_of_payment(response: Response, form_of_payment_id: int, db: Session = Depends(get_db)):
    """Get a form of payment by id"""
    form_of_payment = crud.get_form_of_payment(db, form_of_payment_id)

    if form_of_payment is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return form_of_payment


@router.post("/")
def add_form_of_payment(response: Response, new_form_of_payment: schema.FormOfPaymentCreate, db: Session = Depends(get_db)):
    """Create a new form of payment"""
    try:
        return crud.add_form_of_payment(db, new_form_of_payment)
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return { "error_message": e}
    
@router.delete("/{form_of_payment_id}")
def delete_form_of_payment(response: Response, form_of_payment_id: int, db: Session = Depends(get_db)):
    """Delete a form of payment"""
    if crud.delete_form_of_payment(db, form_of_payment_id) is None:
        response.status_code = status.HTTP_404_NOT_FOUND