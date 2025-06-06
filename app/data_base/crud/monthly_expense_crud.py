from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text, func, or_, and_
from typing import List
from datetime import datetime, timedelta
from ..schemas import monthly_expense_schema
from ..models import monthly_expense_model as model
from ..models import form_of_payment_model
from ..models import expense_category_model
from ..models import balance_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
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
        if new_expense.total_plots > 1:
            # Format the description with the plot number
            description_tmp = new_expense.description.split('(')[0]
            total_plots = new_expense.total_plots if new_expense.total_plots > 9 else f"0{new_expense.total_plots}"
            current_plot = i if i > 9 else f"0{i}"
            plots_string = f"({current_plot}/{total_plots})"
            new_expense.description = description_tmp + plots_string
        
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
            expense_category_id = new_expense.expense_category_id if new_expense.expense_category_id != 24 else await _predict_category_by_description(db, new_expense.description), # 24 is the id of the category "Desconhecido"
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

        if new_expense.status is not None:
            db_expense.status = new_expense.status

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
    expenses = (db.query(
        func.to_char(model.MonthlyExpense.due_date, "yyyy-MM").label("ano_mes"), 
        func.sum(model.MonthlyExpense.amount).label("total")
    )
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

def get_expenses_grouped_by_place(db: Session, due_date: str, status: str):
    """Get all expenses grouped by place

    Parameters:
        db (Session): Session of database
        where (str): This variable is to get a monthly and year at the format "YYYY-mm"

    Returns:
        expenses: Return a query with expenses grouped by place, including the amount.


    """
    due_date = due_date if due_date is not None else datetime.now().strftime("%Y-%m")

    if not status:
        expenses = (
            db.query(
                func.to_char(model.MonthlyExpense.due_date, "yyyy-MM").label("ano_mes"),
                model.MonthlyExpense.place,
                func.sum(model.MonthlyExpense.amount)
            )
            .where(func.to_char(model.MonthlyExpense.due_date, "yyyy-MM") == due_date)
            .group_by(
                func.to_char(model.MonthlyExpense.due_date, "yyyy-MM"),
                model.MonthlyExpense.place
            )
            .all()
        )
    else:
        expenses = (
            db.query(
                func.to_char(model.MonthlyExpense.due_date, "yyyy-MM").label("ano_mes"),
                model.MonthlyExpense.place,
                func.sum(model.MonthlyExpense.amount)
            )
            .where(and_(
                func.to_char(model.MonthlyExpense.due_date, "yyyy-MM") == due_date,
                model.MonthlyExpense.status.like(status)
            ))
            .group_by(
                func.to_char(model.MonthlyExpense.due_date, "yyyy-MM"),
                model.MonthlyExpense.place
            )
            .all()
        )

    expenses_dict = []

    for expense in expenses:
        expenses_dict.append({
            "ano_mes": expense[0],
            "place": expense[1],
            "total": expense[2]
        })
    
    return expenses_dict
 
def get_all_descriptions(db: Session, where: str):
    """Get all descriptions"""
    items = []
    db_descriptions = (db
                    .query(model.MonthlyExpense.description)
                    .where(func.lower(model.MonthlyExpense.description).like(f"{where.lower()}%"))
                    .group_by(model.MonthlyExpense.description)
                    .order_by(model.MonthlyExpense.description)
                    .all())
    count = (db
        .query(model.MonthlyExpense.description)
        .where(func.lower(model.MonthlyExpense.description).like(f"{where.lower()}%"))
        .group_by(model.MonthlyExpense.description)
        .count()
    )

    for description in db_descriptions:
        items.append(description[0])

    descriptions = {
        "total": count,
        "items": items
    }
    

    return descriptions
    
def expense_exist(db: Session, new_expense: monthly_expense_schema.MonthlyExpenseCreate):
    """Check if the expense already exist in database"""
    db_expense = (db.query(model.MonthlyExpense)
                    .where(and_(
                        model.MonthlyExpense.place == new_expense.place,
                        model.MonthlyExpense.amount == new_expense.amount,
                        model.MonthlyExpense.date == new_expense.date,
                        model.MonthlyExpense.total_plots == new_expense.total_plots,
                        model.MonthlyExpense.current_plot == new_expense.current_plot,
                    )))
    
    return db_expense.count() > 0

def expense_not_exist_check_amount(db: Session, new_expense: monthly_expense_schema.MonthlyExpenseCreate):
    """Check if the expense not exist in database and check if the amount is different"""
    db_expense = (db.query(model.MonthlyExpense)
                    .where(and_(
                        model.MonthlyExpense.place == new_expense.place,
                        model.MonthlyExpense.date == new_expense.date,
                        model.MonthlyExpense.total_plots == new_expense.total_plots,
                        model.MonthlyExpense.current_plot == new_expense.current_plot,
                        model.MonthlyExpense.amount != new_expense.amount
                    )).one_or_none())
    
    return db_expense
    
async def _predict_category_by_description(db: Session, description: str):
    """Predict the category of the expense by description"""
    
    # Get all descriptions
    db_categorys = (db.query(
                        model.MonthlyExpense.description, 
                        model.MonthlyExpense.expense_category_id, 
                        expense_category_model.ExpenseCategory.description)
                    .join(expense_category_model.ExpenseCategory)
                    .group_by(
                        model.MonthlyExpense.description, 
                        model.MonthlyExpense.expense_category_id, 
                        expense_category_model.ExpenseCategory.description)
                    .all())
    
    # Set columns to dataframe
    columns = ["description", "category_id", "category"]

    # Create a dataframe
    df_categorys = pd.DataFrame(db_categorys, columns=columns)

    # Create a dictionary with the descriptions and categories
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df_categorys['description'])
    y = df_categorys['category_id']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train the classifier
    clf = SVC(kernel='linear')
    clf.fit(X_train, y_train)

    # Predict by description
    text_vec = vectorizer.transform([description])
    prediction = clf.predict(text_vec)

    category_id = prediction[0]

    return int(category_id)

                    
    
    