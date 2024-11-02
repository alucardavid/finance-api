from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text, func, or_, and_
from typing import List
from datetime import datetime, timedelta
from ..schemas import monthly_expense_schema
from ..models import monthly_expense_model as model
from ..models import form_of_payment_model
from ..models import expense_category_model
from ..models import balance_model
import sys, json

def get_all_expenses(db: Session, page: int = 1, limit: int = 100, order_by: str = "id asc", due_date: str = None, where: str = None):
    """Get all monthly expenses"""
        
    if due_date is None:
        if where is None:
            items = (db.query(model.MonthlyExpense)
                .join(form_of_payment_model.FormOfPayment)
                .join(balance_model.Balance)
                .join(expense_category_model.ExpenseCategory)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments)
                    .joinedload(form_of_payment_model.FormOfPayment.balances))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .order_by(text(order_by))
                .offset((page * limit) - limit)
                .limit(limit).all())
            
            count = db.query(model.MonthlyExpense).count()
        else:
            # Items
            items = (db.query(model.MonthlyExpense)
                .join(form_of_payment_model.FormOfPayment)
                .join(balance_model.Balance)
                .join(expense_category_model.ExpenseCategory)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments)
                    .joinedload(form_of_payment_model.FormOfPayment.balances))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .where(or_(
                    model.MonthlyExpense.place.like(f"%{where}%"),
                    model.MonthlyExpense.description.like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.date, "dd/MM/yyyy").like(f"%{where}%"),
                    func.replace(func.replace(func.replace(func.to_char(model.MonthlyExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.total_plots, "999").like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.current_plot, "999").like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.due_date, "dd/MM/yyyy").like(f"%{where}%"),
                    model.MonthlyExpense.status.like(f"%{where}%"),
                    form_of_payment_model.FormOfPayment.description.like(f"%{where}%")
                )) 
                .order_by(text(order_by))
                .offset((page * limit) - limit)
                .limit(limit).all())
            
            # Count
            count = (db.query(model.MonthlyExpense)
                .join(form_of_payment_model.FormOfPayment)
                .join(balance_model.Balance)
                .join(expense_category_model.ExpenseCategory)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments)
                    .joinedload(form_of_payment_model.FormOfPayment.balances))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .where(or_(
                    model.MonthlyExpense.place.like(f"%{where}%"),
                    model.MonthlyExpense.description.like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.date, "dd/MM/yyyy").like(f"%{where}%"),
                    func.replace(func.replace(func.replace(func.to_char(model.MonthlyExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.total_plots, "999").like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.current_plot, "999").like(f"%{where}%"),
                    func.to_char(model.MonthlyExpense.due_date, "dd/MM/yyyy").like(f"%{where}%"),
                    model.MonthlyExpense.status.like(f"%{where}%"),
                    form_of_payment_model.FormOfPayment.description.like(f"%{where}%")
                )).count())
    else:
        if where is None:
            items = (db.query(model.MonthlyExpense)
                .join(form_of_payment_model.FormOfPayment)
                .join(balance_model.Balance)
                .join(expense_category_model.ExpenseCategory)
                .where(func.to_char(model.MonthlyExpense.due_date, "YYYY-MM") == due_date)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments)
                    .joinedload(form_of_payment_model.FormOfPayment.balances))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .order_by(text(order_by))
                .offset((page * limit) - limit)
                .limit(limit).all())
            
            count = (db.query(model.MonthlyExpense)
                .where(func.to_char(model.MonthlyExpense.due_date, "YYYY-MM") == due_date)
                .count())
        else:
            items = (db.query(model.MonthlyExpense)
                .join(form_of_payment_model.FormOfPayment)
                .join(balance_model.Balance)
                .join(expense_category_model.ExpenseCategory)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments)
                    .joinedload(form_of_payment_model.FormOfPayment.balances))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .where(and_(
                    func.to_char(model.MonthlyExpense.due_date, "YYYY-MM") == due_date, 
                    (or_(
                        model.MonthlyExpense.place.like(f"%{where}%"),
                        model.MonthlyExpense.description.like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.date, "dd/MM/yyyy").like(f"%{where}%"),
                        func.replace(func.replace(func.replace(func.to_char(model.MonthlyExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.total_plots, "999").like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.current_plot, "999").like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.due_date, "dd/MM/yyyy").like(f"%{where}%"),
                        model.MonthlyExpense.status.like(f"%{where}%"),
                        form_of_payment_model.FormOfPayment.description.like(f"%{where}%")
                    )
                )))
                .order_by(text(order_by))
                .offset((page * limit) - limit)
                .limit(limit).all())
            
            count = (db.query(model.MonthlyExpense)
                .join(form_of_payment_model.FormOfPayment)
                .join(balance_model.Balance)
                .join(expense_category_model.ExpenseCategory)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .where(and_(
                    func.to_char(model.MonthlyExpense.due_date, "YYYY-MM") == due_date, 
                    (or_(
                        model.MonthlyExpense.place.like(f"%{where}%"),
                        model.MonthlyExpense.description.like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.date, "dd/MM/yyyy").like(f"%{where}%"),
                        func.replace(func.replace(func.replace(func.to_char(model.MonthlyExpense.amount, "999G999D00"), ",", "v"), ".", ","), "v", ".").like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.total_plots, "999").like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.current_plot, "999").like(f"%{where}%"),
                        func.to_char(model.MonthlyExpense.due_date, "dd/MM/yyyy").like(f"%{where}%"),
                        model.MonthlyExpense.status.like(f"%{where}%"),
                        form_of_payment_model.FormOfPayment.description.like(f"%{where}%")
                    )
                )))
                .count())
    
    
    result = {
        'count': count,
        'total_pages': int((count/ limit)+1),
        'limit': limit,
        'page': page,
        'items': items
    }

    return result

def get_expense_by_id(db: Session, expense_id):
    """Get a expense by id"""
    return (db.query(model.MonthlyExpense)
                .options(
                    joinedload(model.MonthlyExpense.form_of_payments)
                    .joinedload(form_of_payment_model.FormOfPayment.balances))
                .options(joinedload(model.MonthlyExpense.expense_categorys))
                .where(model.MonthlyExpense.id == expense_id).one())

async def create_expense(db: Session, new_expense: monthly_expense_schema.MonthlyExpenseCreate):
    """Create a new expense"""
    expenses = []

    for i in range(new_expense.current_plot, new_expense.total_plots + 1):
        db_expense = model.MonthlyExpense(
            place = new_expense.place,
            description = new_expense.description,
            date = new_expense.date,
            amount = new_expense.amount,
            total_plots = new_expense.total_plots,
            current_plot = i,
            due_date = (new_expense.due_date + timedelta(days=((i-1) * 30))).replace(day=new_expense.due_date.day) if i > 1 else new_expense.due_date,
            status = "Pendente",
            created_at = datetime.now(),
            expense_category_id = new_expense.expense_category_id,
            form_of_payment_id = new_expense.form_of_payment_id,
            user_id = 1
        )
        
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)

        expenses.append(db_expense.__dict__)
    
    return expenses

def delete_expense(db: Session, expense_id: int):
    """Delete a expense"""
    db_expense = db.query(model.MonthlyExpense).get(expense_id)
    if db_expense is not None:
        db.delete(db_expense)
        db.commit()
        return expense_id
    else:
        return None
        
def update_expense(db: Session, expense_id: int, new_expense: monthly_expense_schema.MonthlyExpenseUpdate):
    """Update a expense"""
    db_expense = db.query(model.MonthlyExpense).get(expense_id)

    if db_expense is not None:
        if new_expense.place is not None:
            db_expense.place = new_expense.place
        
        if new_expense.description is not None:
            db_expense.description = new_expense.description

        if new_expense.date is not None:
            db_expense.date = new_expense.date

        if new_expense.amount is not None:
            db_expense.amount = new_expense.amount
        
        if new_expense.total_plots is not None:
            db_expense.total_plots = new_expense.total_plots
        
        if new_expense.current_plot is not None:
            db_expense.current_plot = new_expense.current_plot

        if new_expense.due_date is not None:
            db_expense.due_date = new_expense.due_date
        
        if new_expense.expense_category_id is not None:
            db_expense.expense_category_id = new_expense.expense_category_id

        if new_expense.form_of_payment_id is not None:
            db_expense.form_of_payment_id = new_expense.form_of_payment_id

        db_expense.updated_at = datetime.now()
        db.commit()
        db.refresh(db_expense)

    return db_expense
   
def pay_expense(db: Session, expense_id: int):
    """Change expense status to Pago"""
    db_expense = db.query(model.MonthlyExpense).get(expense_id)

    if db_expense is not None:
        db_expense.status = "Pago"
        db.commit()
        db.refresh(db_expense)
        
    return db_expense

def pay_expenses(db: Session, expenses_id: monthly_expense_schema.MonthlyExpensesPay):
    """Pay all expenses in the list"""
    if expenses_id is not None:
        db.query(model.MonthlyExpense).filter(model.MonthlyExpense.id.in_(expenses_id)).update({"status": "Pago"})
        db.commit()
        
        db_expenses_paid = db.query(model.MonthlyExpense).filter(model.MonthlyExpense.id.in_(expenses_id)).all()
        
    return db_expenses_paid

def get_expenses_grouped_by_month(db: Session, where: str):
    """Get all expenses grouped by month"""
    where = where if where is not None else datetime.now().strftime("%Y-%m")
    expenses = (db.query(func.to_char(model.MonthlyExpense.due_date, "yyyy-MM").label("ano_mes"), func.sum(model.MonthlyExpense.amount).label("total"))
                    .where(func.to_char(model.MonthlyExpense.due_date, "yyyy-MM") >= where)
                    .group_by(func.to_char(model.MonthlyExpense.due_date, "yyyy-MM"))
                    .order_by(func.to_char(model.MonthlyExpense.due_date, "yyyy-MM"), )
                    .all())
    
    expenses_dict = []

    for expense in expenses:
        expenses_dict.append({"ano_mes": expense[0], "total": expense[1]})

    return expenses_dict

def get_expenses_grouped_by_category(db: Session, where: str):
    """Get all expenses grouped by month and category"""
    where = where if where is not None else datetime.now().strftime("%Y-%m")
    expenses = (db
                .query(
                    func.to_char(model.MonthlyExpense.due_date, "yyyy-MM").label("ano_mes"),
                    expense_category_model.ExpenseCategory.description.label("category"),
                    func.sum(model.MonthlyExpense.amount)
                )
                .join(expense_category_model.ExpenseCategory)
                .where(func.to_char(model.MonthlyExpense.due_date, "yyyy-MM") == where)
                .group_by(
                    func.to_char(model.MonthlyExpense.due_date, "yyyy-MM"),
                    expense_category_model.ExpenseCategory.description
                )
                .all())
    
    expenses_dict = []

    for expense in expenses:
        expenses_dict.append({
            "ano_mes": expense[0],
            "category": expense[1],
            "total": expense[2]
        })
    
    return expenses_dict
