
from email import message
from ..scehmas.request_model import Response, CategoryTypeEnum, TransactionResponse,TransactionBase
from sqlalchemy.orm import Session
from ..models.data_model import Bank, Transaction
from sqlalchemy import and_
from fastapi import status


class TransactionService():
    def __init__(self) -> None:
        pass

    def get_all_transactions(self, db: Session, user):
        user_id = user.get("sub")
        print("USER ID__________________", user_id)
        all_transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id).all()
        if len(all_transactions) == 0:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please Add Transactions", result=None)
        print("In Get AL ---------------------------------",
              all_transactions)

        result = [TransactionResponse.from_orm(
            transaction) for transaction in all_transactions]
        print(all_transactions)
        # return all_transactions
        return Response(status_code=status.HTTP_200_OK, is_success=True, message="Get All Transactions Successfully", result=result)

    def create_transaction(self, transaction, db: Session, user):
        user_id = user.get("sub")
        db_transaction = Transaction(user_id=user_id, **transaction)
        db_amount = db_transaction.amount
        if db_amount < 0:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please Enter Positive Amount", result=None)

        db.add(db_transaction)
        update_bank = db.query(Bank).filter(
            and_(Bank.bank_id == db_transaction.bank_id, Bank.user_id == user_id)).first()
        if db_transaction.transaction_type.lower() == CategoryTypeEnum.income:
            update_bank.total_balance += db_transaction.amount
        elif db_transaction.transaction_type.lower() == CategoryTypeEnum.expense:
            update_bank.total_balance -= db_transaction.amount
        db.commit()

        result = self.get_all_transactions(db, user)

        return Response(status_code=status.HTTP_201_CREATED, is_success=True, message="Transaction Added Successfully", result=result.result)

    def delete_transaction(self, id: int, db: Session, user):
        user_id = user.get("sub")
        db_existing_transaction = db.query(Transaction).filter(
            and_(Transaction.transaction_id == id, Transaction.user_id == user_id)).first()
        if not db_existing_transaction:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Transaction does not exist", result=None)

        update_bank = db.query(Bank).filter(
            Bank.bank_id == db_existing_transaction.bank_id).first()
        if db_existing_transaction.transaction_type == CategoryTypeEnum.income:
            update_bank.total_balance -= db_existing_transaction.amount
        elif db_existing_transaction.transaction_type == CategoryTypeEnum.expense:
            update_bank.total_balance += db_existing_transaction.amount

        db.delete(db_existing_transaction)
        db.commit()
        db.refresh(update_bank)
        response = self.get_all_transactions(db, user)
        return Response(status_code=status.HTTP_200_OK, is_success=True, message="Transaction Deleted Successfully", result=response.result)

    def update_transaction(self, id, transaction: TransactionBase, db: Session, user):
        user_id = user.get("sub")
        db_transaction = db.query(Transaction).filter(and_(Transaction.transaction_id == id, Transaction.user_id == user_id)).first()
        if not db_transaction:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Transaction does not exist", result=None)
        update_bank = db.query(Bank).filter(
            Bank.bank_id == db_transaction.bank_id).first()
        if db_transaction.transaction_type == CategoryTypeEnum.income:
            update_bank.total_balance -= db_transaction.amount
        elif db_transaction.transaction_type == CategoryTypeEnum.expense:
            update_bank.total_balance += db_transaction.amount
        
        db.commit()
        db.refresh(update_bank)

        
        db_transaction.amount = transaction.amount
        db_transaction.bank_id = transaction.bank_id
        db_transaction.category_id = transaction.category_id
        db_transaction.subcategory_id = transaction.subcategory_id
        db_transaction.transaction_type = transaction.transaction_type
        db_transaction.transaction_date = transaction.transaction_date
        db_transaction.description = transaction.description

        update_bank = db.query(Bank).filter(
            Bank.bank_id == db_transaction.bank_id).first()
        if transaction.transaction_type == CategoryTypeEnum.income:
            update_bank.total_balance += db_transaction.amount
        elif transaction.transaction_type == CategoryTypeEnum.expense:
            update_bank.total_balance -= db_transaction.amount

        db.commit()
        db.refresh(db_transaction)
        db.refresh(update_bank)
        response = self.get_all_transactions(db, user)
        return Response(status_code=status.HTTP_202_ACCEPTED, is_success=True, message="Transaction Updated Successfully.", result= response.result)


       




transaction_service = TransactionService()
