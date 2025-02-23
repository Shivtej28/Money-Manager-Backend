
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..dao.database import get_db
from typing import List
from ..scehmas.request_model import CreateCategory, UpdateCategory, Response, CategoryResponse
from ..utils.jwtauth import decode_jwt_token
from ..service.categories_service import category_service

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.post("/", response_model=Response)
def createt_category(category: CreateCategory, db: Session = Depends(get_db), user=Depends(decode_jwt_token)):
    response = category_service.create_category(category, db, user)
    print("RESPONSE-----------", response.message)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))


@router.get("/", response_model=Response[List[CategoryResponse]])
def get_all_categories(db: Session = Depends(get_db), user=Depends(decode_jwt_token)):
    response = category_service.get_all_categories(db, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))


@router.put("/{id:int}", response_model=Response)
def update_categories(id: int, category: UpdateCategory, db: Session = Depends(get_db), user=Depends(decode_jwt_token)):
    response = category_service.update_categories(id, db, user, category)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))

# @router.delete("/{id:int}")
# def delete_category(id:int, db:Session = Depends(get_db), user = Depends(decode_jwt_token)):
#     response = category_service.delete_category(id, db, user)
#     return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
