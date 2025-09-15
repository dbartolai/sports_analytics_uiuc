from sqlalchemy import Column, Integer, String
from app.db import Base

class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    major = Column(String, index=True)
    grad_year = Column(Integer, index=True)
    fun_fact = Column(String, nullable=True)
