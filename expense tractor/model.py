from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import  relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    username = Column(String(100), nullable=False,unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False,unique=True)
    expenses = relationship("Expense",back_populates="owner")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    expense_item = Column(String(100), nullable=False)
    expense_category = Column(String(100))
    expense_date = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)
    owner = relationship("User",back_populates="expenses")
