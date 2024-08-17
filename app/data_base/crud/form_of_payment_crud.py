from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text

from typing import List
from datetime import datetime
from ..schemas import form_of_payment_schema as schema
from ..models import form_of_payment_model as model
from ..models import balance_model  

def get_all_form_of_payments(db: Session, skip: int = 0, limit: int = 100, order_by: str = "id asc"):
    """Get all form of payments"""
    form_of_payments = db.query(model.FormOfPayment).options(joinedload(model.FormOfPayment.balances)).order_by(text(order_by)).offset(skip).limit(limit).all()
    
    return form_of_payments

def get_form_of_payment(db: Session, form_of_payment_id: int):
    """Get a form of payment by id"""
    return db.query(model.FormOfPayment).options(joinedload(model.FormOfPayment.balances)).get(form_of_payment_id)

def add_form_of_payment(db: Session, new_form_of_payment: schema.FormOfPaymentCreate):
    """Create a new form of payment"""
    db_form_of_payment = model.FormOfPayment(
        description = new_form_of_payment.description,
        balance_id = new_form_of_payment.balance_id,
        created_at = datetime.now()
    )

    db.add(db_form_of_payment)
    db.commit()
    db.refresh(db_form_of_payment)

    return db_form_of_payment

def delete_form_of_payment(db: Session, form_of_payment_id: int):
    """Delete a form of payment"""
    db_form_of_payment = db.query(model.FormOfPayment).get(form_of_payment_id)
    if db_form_of_payment is not None:
        db.delete(db_form_of_payment)
        db.commit()

        return form_of_payment_id
    else:
        return None

    
    