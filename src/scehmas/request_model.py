from fastapi import Query
from pydantic import BaseModel, EmailStr

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

class User(UserBase):
    id : int

    class Config:
        orm_mode = True

