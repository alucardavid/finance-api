from sqlalchemy.orm import Session
from datetime import datetime
from ..models import incoming_model as model
from sqlalchemy.sql import text

def get_incomings(db: Session, status: str = "Pendente", order_by: str = "id asc"):
    """Get all incomings"""
    incomings = (db.query(model.Incoming)
                        .where(model.Incoming.status == status)
                        .order_by(text(order_by))
                        .all())  

    return incomings