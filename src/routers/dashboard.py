
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..dao.database import get_db
from ..utils.jwtauth import decode_jwt_token
from ..service.dashboard_service import dashboard_service
from ..scehmas.request_model import DashboardBank, MainDashboardResponse, Response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=Response[DashboardBank])
def bank_dashboard(db: Session = Depends(get_db),  user=Depends(decode_jwt_token)):
    response = dashboard_service.get_all_details(db, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))


@router.get("/income-expense", response_model=Response[MainDashboardResponse])
def main_dashboard(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db), user=Depends(decode_jwt_token)):
    if start_date == None and end_date == None:
        current_date = date.today()
        start_date = date(current_date.year, current_date.month, 1)
        end_date = date(current_date.year, current_date.month,
                        28) + timedelta(days=4)
        end_date = end_date.replace(day=1) - timedelta(days=1)

    print(start_date)
    print(end_date)
    response = dashboard_service.main_dashboard(start_date, end_date,db, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
