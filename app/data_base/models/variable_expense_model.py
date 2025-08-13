from sqlalchemy import Column, Integer, String, DateTime, Numeric, BigInteger, Sequence, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database import Base

class VariableExpense(Base):
    __tablename__= "variable_expenses"

    id = Column(BigInteger, Sequence("variable_expenses_id_seq"), primary_key=True, autoincrement=True)
    date = Column(DateTime)
    place = Column(String)
    description = Column(String)
    type = Column(String)
    amount = Column(Numeric)
    created_at = Column(DateTime)
    updated_at = Column(Integer)
    form_of_payment_id = Column(Integer, ForeignKey("form_of_payments.id"))
    user_id = Column(Integer)
    id_transaction = Column(String, nullable=True)
    form_of_payments = relationship("FormOfPayment", back_populates="variable_expenses")
    
