from sqlalchemy import Column, Integer, String, DateTime, Numeric, BigInteger, Sequence, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import List
from .balance_model import Balance

from ..database import Base

class FormOfPayment(Base):
    __tablename__= "form_of_payments"

    id = Column(BigInteger, Sequence("form_of_payments_id_seq"), primary_key=True, autoincrement=True)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    balance_id = Column(Integer, ForeignKey("balances.id"))
    active = Column(String)
    balances = relationship("Balance", back_populates="form_of_payments")
    variable_expenses = relationship("VariableExpense", back_populates="form_of_payments")
    