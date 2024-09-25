
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dao.database import get_db
from ..scehmas.request_model import CreateCategory
from ..utils.jwtauth import decode_jwt_token

router = APIRouter(prefix="/api/categeroies", tags=["Categories"])


@router.post("/")
def createt_category(category: CreateCategory , db : Session = Depends(get_db), user = Depends(decode_jwt_token)):
    return True