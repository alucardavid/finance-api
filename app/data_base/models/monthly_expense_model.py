from sqlalchemy import Column, Integer, String, DateTime, Numeric, BigInteger, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from .form_of_payment_model import FormOfPayment

from ..database import Base

class MonthlyExpense(Base):
    __tablename__= "monthly_expenses"

    id = Column(BigInteger, Sequence("monthly_expenses_id_seq"), primary_key=True, autoincrement=True)
    place = Column(String)
    description = Column(String)
    date = Column(DateTime)
    amount = Column(Numeric)
    total_plots = Column(Integer)
    current_plot = Column(Integer)
    due_date = Column(DateTime)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    expense_category_id = Column(Integer, ForeignKey("expense_categorys.id"))
    form_of_payment_id = Column(Integer, ForeignKey("form_of_payments.id"))
    user_id = Column(Integer)
    form_of_payments = relationship("FormOfPayment", back_populates="monthly_expenses")
    expense_categorys = relationship("ExpenseCategory", back_populates="monthly_expenses")

