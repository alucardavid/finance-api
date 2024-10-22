from sqlalchemy.orm import Session
from datetime import datetime
from ..models import expense_category_model as model
from ..schemas import expense_category_schema as schema
from sqlalchemy.sql import text, func, or_, and_

def get_expense_categorys(db: Session, page: int = 1, limit: int = 100, order_by: str = "id asc", where: str = None):
    """Get all expense categorys"""
    if not where:
        categorys = (db.query(model.ExpenseCategory)
                       .order_by(text(order_by))
                       .offset((page * limit) - limit)
                       .limit(limit)
                       .all())  
        count = (db.query(model.ExpenseCategory).count())
    else:
        categorys = (db.query(model.ExpenseCategory)
                       .where(or_(
                           model.ExpenseCategory.description.like(f"%{where}%"),
                           model.ExpenseCategory.show.like(f"%{where}%")
                       ))
                       .order_by(text(order_by))
                       .offset((page * limit) - limit)
                       .limit(limit)
                       .all())  
        count = (db.query(model.ExpenseCategory)
                   .where(or_(
                        model.ExpenseCategory.description.like(f"%{where}%"),
                        model.ExpenseCategory.show.like(f"%{where}%")
                   )).count())

    result = {
        'count': count,
        'total_pages': int((count/ limit)+1),
        'limit': limit,
        'page': page,
        'items': categorys
    }

    return result

def get_expense_categorys_by_id(db: Session, expense_category_id: int):
    """Get expense category by id"""

    expese_category = db.query(model.ExpenseCategory).get(expense_category_id)

    return expese_category

def create_expense_category(db: Session, new_category: schema.ExpenseCategory):
    """Create a new expense category"""

    db_category = model.ExpenseCategory(
        description = new_category.description,
        show = new_category.show,
        created_at = datetime.now()
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

def delete_expense_category(db: Session, category_id: int):
    """Delete a expense category"""

    db_category = db.query(model.ExpenseCategory).get(category_id)

    if not db_category:
        return None
    else:
        db.delete(db_category)
        db.commit()

        return category_id
    
def update_expense_category(db: Session, category_id: int, new_category: schema.ExpenseCategoryUpdate):
    """Update a expense category by id"""

    db_category = db.query(model.ExpenseCategory).get(category_id)

    if not db_category:
        return None
    else:
        if new_category.description is not None:
            db_category.description = new_category.description
        
        if new_category.show is not None:
            db_category.show = new_category.show
        
        db_category.updated_at = datetime.now()
        db.commit()
        db.refresh(db_category)

        return db_category
