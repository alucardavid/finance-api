from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text

from typing import List
from datetime import datetime
from ..schemas import form_of_payment_schema as schema
from ..models import form_of_payment_model
from ..models import balance_model  

def get_all_form_of_payments(db: Session, skip: int = 0, limit: int = 100, order_by: str = "id asc"):
    """Get all form of payments"""
    form_of_payments = db.query(form_of_payment_model.FormOfPayment).options(joinedload(form_of_payment_model.FormOfPayment.balances)).order_by(text(order_by)).offset(skip).limit(limit).all()
    
    return form_of_payments


    
    