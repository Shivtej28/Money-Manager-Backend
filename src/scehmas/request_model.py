from typing import List, Optional
from unicodedata import category
from fastapi import Query
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password_hash: str

class UserLogin(BaseModel):
    email: EmailStr = Query(..., description="email")
    password_hash: str = Query(..., description="password")

class GetUser(BaseModel):
    email: EmailStr
    username: str
    token: str

class User(UserBase):
    id : int

    class Config:
        orm_mode = True

class CeateCategory(BaseModel):
    category: str
    subcategory : List[str]
    type_of: str

class CreateBank(BaseModel):
    bank_name : str
    account_type: str
    total_balance: float

class Bank(CreateBank):
    bank_id: int
    user_id: int

    class Config:
        orm_mode = True

class CategoryTypeEnum(str, Enum):
    income = "income"
    expense = "expense"

class CreateSubCategory(BaseModel):
    subcategory_name : str
    type_of: CategoryTypeEnum

class CreateCategory(BaseModel):
    category_name : str
    type_of: CategoryTypeEnum
    sub_category : Optional[List[CreateSubCategory]]  


