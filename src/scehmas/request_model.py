from datetime import date, datetime
from typing import List, Optional
from unicodedata import category
from fastapi import Query
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Generic, TypeVar, List, Optional
from pydantic.generics import GenericModel

# Declare a generic type variable for result
T = TypeVar("T")

class Response(GenericModel, Generic[T]):
    is_success: bool
    result: Optional[T]  # The result can be any type of data
    message: str
    status_code: int

    class Config:
        schema_extra = {
            "example": {
                "is_success": False,
                "result": {},
                "message": "Success",
                "status_code": 200
            }
        }


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

class CategoryTypeEnum(str, Enum):
    income = "income"
    expense = "expense"

class CreateSubCategory(BaseModel):
    subcategory_name : str

class CreateCategory(BaseModel):
    category_name: str
    sub_categories : List[str]
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

class UpdateSubCategory(CreateSubCategory):
    id: int

class UpdateCategory(BaseModel):
    category_name : str
    type_of: CategoryTypeEnum
    sub_category : Optional[List[UpdateSubCategory]]

class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    type_of: str
    subcategories: List[UpdateSubCategory]


class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    transaction_date: date
    description: str = ""
    bank_id: int
    category_id: int = None
    subcategory_id: int = None

    class Config:
        from_attributes = True

class TransactionResponse(TransactionBase):
    transaction_id: int
    user_id: int










