
from fastapi import status
from sqlalchemy.orm import Session
from ..models.data_model import Bank
from ..utils.response import Response
from ..scehmas.request_model import CreateBank

class BankService:
    def __init__(self) -> None:
        pass

    def get_all_banks(self, db: Session, user):
        user_id = user.get("sub")
        all_banks = db.query(Bank).filter(Bank.user_id == user_id).all()
        if len(all_banks) == 0:
            return Response(status_code=status.HTTP_404_NOT_FOUND, is_success=False, message="Please add Bank Details")
        return Response(status_code=status.HTTP_200_OK, is_success= True, message="Get All banks Successfully", result=all_banks)

    def create_bank(self, db: Session, request_model, user):
        bank_to_create = Bank(user_id = user.get("sub"), **request_model)
        db.add(bank_to_create)
        db.commit()
        result = self.get_all_banks(db, user)
        return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="Bank Detail Added Successfully", result=result.result)

    def update_bank(self, db: Session, request_model: CreateBank, user, id):
        bank = db.query(Bank).filter(Bank.bank_id == id).first()
        if not bank:
            return Response(status_code=status.HTTP_404_NOT_FOUND, is_success=False, message="Bank Does not Exists", result = None)
        bank.account_type = request_model.account_type
        bank.bank_name = request_model.bank_name
        bank.total_balance = request_model.total_balance

        db.commit()
        db.refresh(bank)

        result = self.get_all_banks(db, user)
        return Response(status_code=status.HTTP_200_OK, is_success= True, message="Bank Detail Updated Successfully", result=result.result)
    
    def delete_bank(self, db : Session, user, id):
        bank = db.query(Bank).filter(Bank.bank_id == id).first()
        if not bank:
            return Response(status_code=status.HTTP_404_NOT_FOUND, is_success=False, message="Bank Does not Exists")
        db.delete(bank)
        db.commit()
        result = self.get_all_banks(db, user)
        return Response(status_code=status.HTTP_200_OK, is_success= True, message="Bank Detail Updated Successfully", result=result.result)


bank_service = BankService()

