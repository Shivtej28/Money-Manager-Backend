from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, DateTime
from sqlalchemy.orm import relationship
from ..dao.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    category_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type_of = Column(String)

    subcategories = relationship("Subcategory", back_populates="category")

class Subcategory(Base):
    __tablename__ = "subcategories"
    subcategory_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    subcategory_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type_of = Column(String)

    category = relationship("Category", back_populates="subcategories")
    transactions = relationship("Transaction", back_populates="subcategory")

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    subcategory_id = Column(Integer, ForeignKey('subcategories.subcategory_id'))
    amount = Column(Float)
    transaction_type = Column(String)  # 'income' or 'expense'
    transaction_date = Column(Date)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    subcategory = relationship("Subcategory", back_populates="transactions")

class Loan(Base):
    __tablename__ = "loans"
    loan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    loan_type = Column(String)
    principal_amount = Column(Float)
    interest_rate = Column(Float)
    loan_term = Column(Integer)  # in years
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Investment(Base):
    __tablename__ = "investments"
    investment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    investment_type = Column(String)
    amount = Column(Float)
    start_date = Column(Date)
    maturity_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Bank(Base):
    __tablename__ = "banks"
    bank_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    bank_name = Column(String)
    total_balance = Column(Float)
    account_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
