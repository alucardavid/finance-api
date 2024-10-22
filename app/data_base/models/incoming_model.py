from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, Sequence
from sqlalchemy.orm import relationship, Mapped
from ..database import Base

class Incoming(Base):
    __tablename__ = "incomings"

    id = Column(BigInteger, Sequence("incoming_id_seq"), primary_key=True, autoincrement=True)
    description = Column(String)
    amount = Column(Numeric)
    source = Column(String)
    date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(String)