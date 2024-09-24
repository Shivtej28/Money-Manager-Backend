
from fastapi import status
from sqlalchemy.orm import Session
from ..models.data_model import Bank
from ..utils.response import Response

class BankService:
    def __init__(self) -> None:
        pass

    def get_all_banks(self, db: Session, user):
        user_id = user.get("sub")
        all_banks = db.query(Bank).filter(Bank.user_id == user_id).all()
        print(all_banks)
        return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="Get ALl banks Successfully", result=all_banks )

    def create_bank(self, db: Session, request_model, user):
        bank_to_create = Bank(user_id = user.get("sub"), **request_model)
        db.add(bank_to_create)
        db.commit()
        result = self.get_all_banks(db, user)
        return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="bank Detail Added Successfully", result=result.result )

    

bank_service = BankService()

