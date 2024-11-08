from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import incoming_model as model
from ..data_base.crud import incoming_crud as crud
from ..data_base.schemas import incoming_schema as schema
from ..data_base.database import SessionLocal, engine, get_db

model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/", status_code=201)
def read_incomings(
    status: str = None, page: int = 1, limit: int = 50, order_by: str = "id asc", where: str = None, 
    type_return: str = "standard", db: Session = Depends(get_db)):
    """Retrieve all incomings"""

    match type_return:
        case "standar":
            incomings = crud.get_incomings(db, page, limit, status, order_by, where)
        case "grouped_by_month":
            incomings = crud.get_incomings_grouped_by_month(db, where)

    return incomings

@router.get("/{incoming_id}")
def read_incoming_by_id(incoming_id: str, response: Response, db: Session = Depends(get_db)):
    """Retrieve incoming by id"""
    incoming = crud.get_incoming_by_id(db, incoming_id)

    if not incoming:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
    else:
        return incoming
    
@router.post("/")
def create_incoming(new_incoming: schema.IncomingCreate, db: Session = Depends(get_db)):
    """Create a new incoming"""
    return crud.create_incoming(db, new_incoming)

@router.delete("/{incoming_id}")
def delete_incoming(incoming_id: int, response: Response, db: Session = Depends(get_db)):
    """Delete a incoming"""
    incoming = crud.delete_incoming(db, incoming_id)
    
    if not incoming:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_204_NO_CONTENT

@router.put("/{incoming_id}")
def update_incoming(incoming_id: int, response: Response, new_incoming: schema.IncomingUpdate, db: Session = Depends(get_db)):
    """Update a incoming"""
    return crud.update_incoming(db, incoming_id, new_incoming)

