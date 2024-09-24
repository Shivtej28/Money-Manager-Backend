
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from ..scehmas.request_model import CreateBank
from sqlalchemy.orm import Session
from ..dao.database import get_db
from ..utils.jwtauth import decode_jwt_token
from ..service.bank_service import bank_service
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/api/bank", tags=['Bank'])

@router.post("/")
def create_bank(bank : CreateBank, db: Session = Depends(get_db), user = Depends(decode_jwt_token)):
    bank_to_create = bank.dict()
    response = bank_service.create_bank(db, bank_to_create, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))

@router.get("/")
def get_all_banks(db: Session = Depends(get_db), user = Depends(decode_jwt_token)):
    response = bank_service.get_all_banks(db, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response)) 