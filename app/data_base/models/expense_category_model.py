from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, Sequence
from sqlalchemy.orm import relationship, Mapped
from ..database import Base

class ExpenseCategory(Base):
    __tablename__ = "expense_categorys"

    id = Column(BigInteger, Sequence("expense_category_id_seq"), primary_key=True, autoincrement=True)
    description = Column(String)
    show = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)