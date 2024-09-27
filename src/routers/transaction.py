
from re import S
from urllib import response
from fastapi import APIRouter, Depends
from ..dao.database import get_db
from sqlalchemy.orm import Session
from ..utils.jwtauth import decode_jwt_token
from ..scehmas.request_model import TransactionBase, TransactionResponse, Response
from ..service.transactioin_service import transaction_service
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTcyNzUwODkyOH0.bloAuZfhrNj_ODh5vIFqUsJXEYTUUbfmqYFOG0BCI14"
router = APIRouter(prefix="/api/transactions", tags=['Transactions'])


@router.get("/", response_model=Response[List[TransactionResponse]])
def get_all_transactions(db:Session = Depends(get_db), user = Depends(decode_jwt_token)):
    response = transaction_service.get_all_transactions(db, user)
    
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))

@router.post("/")
def create_transaction(transaction: TransactionBase , db: Session = Depends(get_db), user = Depends(decode_jwt_token)):
    add_transaction = transaction.dict()
    response = transaction_service.create_transaction(add_transaction,db, user)
    print("IN API_--------------------")
    #print(response)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))

@router.put("/{id}")
def update_transaction(id: int, transaction: TransactionBase, db:Session = Depends(get_db), user = Depends(decode_jwt_token)):
    response = transaction_service.update_transaction(id, transaction, db, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))

@router.delete("/{id}")
def delete_transaction(id: int, db:Session = Depends(get_db), user = Depends(decode_jwt_token)):
    response = transaction_service.delete_transaction(id, db, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
