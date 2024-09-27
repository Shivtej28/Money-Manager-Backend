
from fastapi import APIRouter, Depends
from ..dao.database import get_db
from sqlalchemy.orm import Session
from ..utils.jwtauth import decode_jwt_token
from ..scehmas.request_model import TransactionBase, TransactionResponse, Response
from ..service.transactioin_service import transaction_service
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTcyNzQ0NDEyNH0.rxEsLgvxJuj3ZyH6r98KM5zOAR-43gsK_1joQRz9BJQ"
router = APIRouter(prefix="/api/transactions", tags=['Transactions'])

@router.post("/")
def create_transaction(transaction: TransactionBase , db: Session = Depends(get_db), user = Depends(decode_jwt_token)):
    add_transaction = transaction.dict()
    response = transaction_service.create_transaction(add_transaction,db, user)
    print("IN API_--------------------")
    #print(response)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))

@router.get("/", response_model=Response[List[TransactionResponse]])
def get_all_transactions(db:Session = Depends(get_db), user = Depends(decode_jwt_token)):
    response = transaction_service.get_all_transactions(db, user)
    
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
