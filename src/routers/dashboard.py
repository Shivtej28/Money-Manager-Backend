
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..dao.database import get_db
from ..utils.jwtauth import decode_jwt_token
from ..service.dashboard_service import dashboard_service
from ..scehmas.request_model import MainDashboardResponse, Response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=Response[MainDashboardResponse])
def main_dashboard(db:Session = Depends(get_db), user = Depends(decode_jwt_token)):
    response = dashboard_service.main_dashboard(db, user)
    return JSONResponse(status_code = response.status_code, content = jsonable_encoder(response))
