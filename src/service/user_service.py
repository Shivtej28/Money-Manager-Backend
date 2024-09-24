from fastapi import status
from sqlalchemy.orm import Session
from ..models.data_model import User
from ..scehmas.request_model import GetUser
from ..utils.response import Response
from fastapi.encoders import jsonable_encoder

class UserService():
    def __init__(self) -> None:
        pass

    def create_user(self, db: Session, requets_model):
        user = User(username=requets_model.get('username'), email = requets_model.get('email'), password_hash = requets_model.get('password_hash'))
        existing_user = db.query(User).filter(user.email == User.email).first()
        if existing_user:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success= False, message="User already exist. Please Login" )
        db.add(user)
        db.commit()
        result = GetUser(username=user.username, email=user.email)
        return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="User Ccreated Successfull", result=result.dict())

    def login_user(self, db: Session, request_model):
        email = request_model.get('email')
        password = request_model.get('password_hash')
        existing_user = db.query(User).filter(email == User.email).first()
        if not existing_user:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success= False, message="User does not exist. Please Sign up" )
        if existing_user.password_hash == password:
            result = GetUser(username=existing_user.username, email=existing_user.email)
            return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="Login Succesfully", result=result.dict())
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success= False, message="Please insert correct email id or password")

user_service = UserService()