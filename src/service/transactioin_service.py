from email import message
from unittest import result
from ..scehmas.request_model import Response, CategoryTypeEnum, TransactionResponse
from sqlalchemy.orm import Session
from ..models.data_model import Bank, Transaction
from sqlalchemy import and_
from fastapi import status

class TransactionService():
    def __init__(self) -> None:
        pass

    def get_all_transactions(self, db: Session, user):
        user_id = user.get("sub")
        all_transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        if all_transactions.count == 0:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please Add Transactions", result=None)
        print("In Get AL ---------------------------------")
        print(all_transactions[0].__dict__)
        result = [TransactionResponse.from_orm(transaction) for transaction in all_transactions]
        
        #return all_transactions
        return Response(status_code = status.HTTP_200_OK, is_success=True, message="Get All Transactions Successfully", result=result)

    def create_transaction(self, transaction, db: Session, user):
        user_id = user.get("sub")
        db_transaction = Transaction(user_id = user_id, **transaction)
        db_amount = db_transaction.amount
        if db_amount < 0:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please Enter Positive Amount", result=None)

        db.add(db_transaction)
        update_bank = db.query(Bank).filter(and_(Bank.bank_id == db_transaction.bank_id, Bank.user_id == user_id)).first()
        if db_transaction.transaction_type.lower() == CategoryTypeEnum.income:
            update_bank.total_balance += db_transaction.amount
        elif db_transaction.transaction_type.lower() == CategoryTypeEnum.expense:
            update_bank.total_balance -= db_transaction.amount
        db.commit()
        
        result = self.get_all_transactions(db, user)

        print("--------------------------")
       # print(result)
        return Response(status_code=status.HTTP_201_CREATED, is_success= True, message="Transaction Added Successfully", result=result.result)

    


transaction_service = TransactionService()