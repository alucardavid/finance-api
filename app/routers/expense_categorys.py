from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..data_base.models import expense_category_model as model
from ..data_base.schemas import expense_category_schema as schema
from ..data_base.crud import expense_category_crud as crud
from ..data_base.database import engine, get_db
from typing import List, Optional

model.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def read_expense_categorys(page: int = 1, limit: int = 50, order_by: str = "id asc", where: str = None, db: Session = Depends(get_db)):
    """Retrive all categorys"""

    expense_categorys = crud.get_expense_categorys(db, page, limit, order_by, where)

    return expense_categorys

@router.get("/{expense_category_id}")
def read_expense_category_by_id(expense_category_id: int, response: Response, db: Session = Depends(get_db)):
    """Get a expense category by id"""

    expense_category = crud.get_expense_categorys_by_id(db, expense_category_id)

    if not expense_category:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
    else:
        return expense_category

@router.post("/")
def create_expense_category(new_category: schema.ExpenseCategoryCreate, db: Session = Depends(get_db)):
    """Create a new expense category"""
    return crud.create_expense_category(db, new_category)

@router.delete("/{category_id}")
def delete_expense_category(category_id: int, response: Response, db: Session = Depends(get_db)):
    """Delete a expense category"""
    category = crud.delete_expense_category(db, category_id)

    if not category:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_204_NO_CONTENT

@router.put("/{category_id}")
def update_expense_category(category_id: int, response: Response, new_category: schema.ExpenseCategoryUpdate, db: Session = Depends(get_db)):
    """Update a expense category"""
    return crud.update_expense_category(db, category_id, new_category)

