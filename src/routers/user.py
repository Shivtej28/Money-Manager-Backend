from typing import Annotated
from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..scehmas.request_model import UserBase, UserLogin
from ..dao.database import get_db
from ..service.user_service import user_service

router = APIRouter(prefix="/api", tags=['User'])


@router.post("/user/create")
def create_user(user : UserBase, db : Session =  Depends(get_db)):
    user_to_create = user.dict()
    response = user_service.create_user(db, user_to_create)
    return JSONResponse(status_code = response.status_code, content = jsonable_encoder(response))

@router.get("/user/login")
def login_user(user: UserLogin = Depends() , db: Session = Depends(get_db)):
    user_to_login = user.dict()
    response = user_service.login_user(db, user_to_login)
    return JSONResponse(status_code = response.status_code, content = jsonable_encoder(response))

