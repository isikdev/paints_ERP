from sqlalchemy import Column, Integer, String

from .base_model import Base


class Counterparty(Base):
    __tablename__ = "counterparties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    inn = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=True)
