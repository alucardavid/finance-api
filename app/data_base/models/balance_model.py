from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, BigInteger, Sequence
from sqlalchemy.orm import relationship, Mapped
from ..database import Base

class Balance(Base):
    __tablename__ = "balances"

    id = Column(BigInteger, Sequence('balances_id_seq'),  primary_key=True, autoincrement=True)
    description = Column(String)
    value = Column(Numeric)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
    user_id = Column(Integer)
    show = Column(String)
    form_of_payments = relationship("FormOfPayment", back_populates="balances")