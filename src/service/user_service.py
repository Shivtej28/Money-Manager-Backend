from fastapi import status
from sqlalchemy.orm import Session
from ..models.data_model import User
from ..scehmas.request_model import GetUser
from ..utils.response import Response
from fastapi.encoders import jsonable_encoder
from ..utils.jwtauth import create_access_token

class UserService():
    def __init__(self) -> None:
        pass

    def create_user(self, db: Session, requets_model):
        user = User(username=requets_model.get('username'), email = requets_model.get('email'), password_hash = requets_model.get('password_hash'))
        existing_user = db.query(User).filter(user.email == User.email).first()
        if existing_user:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success= False, message="User already exist. Please Login", result=None)
        db.add(user)
        db.commit()
        payload =  {"sub": user.user_id}
        token = create_access_token(payload=payload)
        result = GetUser(username=user.username, email=user.email, token=token)
        return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="User Created Successfully", result=result.dict())

    def login_user(self, db: Session, request_model):
        email = request_model.get('email')
        password = request_model.get('password_hash')
        existing_user = db.query(User).filter(email == User.email).first()
        if not existing_user:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success= False, message="User does not exist. Please Sign up", result=None )
        if existing_user.password_hash == password:
            payload =  {"sub": existing_user.user_id}
            token = create_access_token(payload=payload)
            result = GetUser(username=existing_user.username, email=existing_user.email, token=token)
            return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="Login Succesfully", result=result)
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success= False, message="Please insert correct email id or password", result = None)

user_service = UserService()