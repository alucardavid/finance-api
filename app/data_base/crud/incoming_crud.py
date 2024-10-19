from sqlalchemy.orm import Session
from datetime import datetime
from ..models import incoming_model as model
from ..schemas import incoming_schema as schema
from sqlalchemy.sql import text

def get_incomings(db: Session, status: str = "Pendente", order_by: str = "id asc"):
    """Get all incomings"""
    incomings = (db.query(model.Incoming)
                        .where(model.Incoming.status == status)
                        .order_by(text(order_by))
                        .all())  

    return incomings

def get_incoming_by_id(db: Session, incoming_id: int):
    """Get a incoming by id"""
    incoming = db.query(model.Incoming).get(incoming_id)

    return incoming

def create_incoming(db: Session, new_incoming: schema.IncomingCreate):
    """Create a new incoming"""
    db_incoming = model.Incoming(
        description = new_incoming.description,
        amount = new_incoming.amount,
        source = new_incoming.source,
        date = new_incoming.date,
        status = new_incoming.status if new_incoming.status is not None else "Pendente",
        created_at = datetime.now()
    )

    db.add(db_incoming)
    db.commit()
    db.refresh(db_incoming)

    return db_incoming

def delete_incoming(db: Session, incoming_id: int):
    """Delete a incoming by id"""

    db_incoming = db.query(model.Incoming).get(incoming_id)

    if not db_incoming:
        return None
    else:
        db.delete(db_incoming)
        db.commit()

        return incoming_id
    
def update_incoming(db: Session, incoming_id: int, new_incoming: schema.IncomingUpdate):
    """Update a incoming by id"""

    db_incoming = db.query(model.Incoming).get(incoming_id)

    if not db_incoming:
        return None
    else:
        if new_incoming.description is not None:
            db_incoming.description = new_incoming.description

        if new_incoming.amount is not None:
            db_incoming.amount = new_incoming.amount
        
        if new_incoming.source is not None:
            db_incoming.source = new_incoming.source

        if new_incoming.date is not None:
            db_incoming.date = new_incoming.date

        if new_incoming.status is not None:
            db_incoming.status = new_incoming.status

        db_incoming.updated_at = datetime.now()
        db.commit()
        db.refresh(db_incoming)

        return db_incoming

