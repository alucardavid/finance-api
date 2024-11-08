from sqlalchemy.orm import Session
from datetime import datetime
from ..models import incoming_model as model
from ..schemas import incoming_schema as schema
from sqlalchemy.sql import text, func, or_, and_

def get_incomings(db: Session, page: int = 1, limit: int = 100, status: str = None, order_by: str = "id asc", where: str = None):
    """Get all incomings"""
    if not status:
        if not where:
            incomings = (db.query(model.Incoming)
                           .order_by(text(order_by))
                           .offset((page * limit) - limit)
                           .limit(limit)
                           .all())  
            count = (db.query(model.Incoming).count())
        else:
            incomings = (db.query(model.Incoming)
                           .where(or_(
                               model.Incoming.description.like(f"%{where}%"),
                               model.Incoming.source.like(f"%{where}%"),
                               model.Incoming.status.like(f"%{where}%"),
                               func.to_char(model.Incoming.date, "dd/MM/yyyy").like(f"%{where}%"),
                               func.replace(func.replace(func.replace(func.to_char(model.Incoming.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    
                           ))
                           .order_by(text(order_by))
                           .offset((page * limit) - limit)
                           .limit(limit)
                           .all()) 
             
            count = (db.query(model.Incoming)
                       .where(or_(
                        model.Incoming.description.like(f"%{where}%"),
                        model.Incoming.source.like(f"%{where}%"),
                        model.Incoming.status.like(f"%{where}%"),
                        func.to_char(model.Incoming.date, "dd/MM/yyyy").like(f"%{where}%"),
                        func.replace(func.replace(func.replace(func.to_char(model.Incoming.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    )).count())
    else:
        if not where:
            incomings = (db.query(model.Incoming)
                        .where(model.Incoming.status == status)
                        .order_by(text(order_by))
                        .offset((page * limit) - limit)
                        .limit(limit)
                        .all())  
            count = db.query(model.Incoming).where(model.Incoming.status == status).count()

        else:
            incomings = (db.query(model.Incoming)
                           .where(and_(
                               model.Incoming.status == status,
                               (or_(
                               model.Incoming.description.like(f"%{where}%"),
                               model.Incoming.source.like(f"%{where}%"),
                               model.Incoming.status.like(f"%{where}%"),
                               func.to_char(model.Incoming.date, "dd/MM/yyyy").like(f"%{where}%"),
                               func.replace(func.replace(func.replace(func.to_char(model.Incoming.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    
                               )
                           )))
                           .order_by(text(order_by))
                           .offset((page * limit) - limit)
                           .limit(limit)
                           .all()) 
             
            count = (db.query(model.Incoming)
                       .where(and_(
                               model.Incoming.status == status,
                               (or_(
                               model.Incoming.description.like(f"%{where}%"),
                               model.Incoming.source.like(f"%{where}%"),
                               model.Incoming.status.like(f"%{where}%"),
                               func.to_char(model.Incoming.date, "dd/MM/yyyy").like(f"%{where}%"),
                               func.replace(func.replace(func.replace(func.to_char(model.Incoming.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    
                               )
                           ))).count())


    result = {
        'count': count,
        'total_pages': int((count/ limit)+1),
        'limit': limit,
        'page': page,
        'items': incomings
    }

    return result

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

def get_incomings_grouped_by_month(db: Session, where: str):
    """Get all incomings grouped by month"""
    where = where if where is not None else datetime.now().strftime("%Y-%m")
    incomings = (db.query(
        func.to_char(model.Incoming.date, "yyyy-MM").label("ano_mes"),
        func.sum(model.Incoming.amount).label("total")
    )
    .where(
        func.to_char(model.Incoming.date, "yyyy-MM") >= where,
        model.Incoming.status == "Pendente"
    )
    .group_by(func.to_char(model.Incoming.date, "yyyy-MM"))
    .order_by(func.to_char(model.Incoming.date, "yyyy-MM"))
    .all())

    incomings_dict = []

    for incoming in incomings:
        incomings_dict.append({
            "anoe_mes": incoming[0],
            "total": incoming[1]
        })
    
    return incomings_dict