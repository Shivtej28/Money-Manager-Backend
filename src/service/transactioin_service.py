
from typing import List
from ..scehmas.request_model import Response, CategoryTypeEnum, TransactionResponse, TransactionBase, UploadTransaction, TransactionResponseNew
from sqlalchemy.orm import Session
from ..models.data_model import Bank, Transaction
from sqlalchemy import and_, exists
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

        result = [
            TransactionResponseNew(
                transaction_id=t.transaction_id,
                user_id=t.user_id,
                amount=t.amount,
                transaction_type=t.transaction_type,
                transaction_date=t.transaction_date,
                description=t.description,
                bank_id=t.bank.bank_name,
                category_id=t.category.category_name,
                subcategory_id=t.subcategory.subcategory_name

            )
            for t in all_transactions]
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
        db_transaction = db.query(Transaction).filter(
            and_(Transaction.transaction_id == id, Transaction.user_id == user_id)).first()
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
        return Response(status_code=status.HTTP_202_ACCEPTED, is_success=True, message="Transaction Updated Successfully.", result=response.result)

    def upload_file(self, transactions: List[UploadTransaction], db: Session, user):
        user_id = user.get("sub")

        # List to store transactions that need to be inserted (non-duplicate)
        add_transactions = []

        # Loop through the transactions
        for obj in transactions:
            # Check if the transaction already exists (based on fields like amount, date, description)
            is_existing = db.query(exists().where(
                Transaction.user_id == user_id,
                Transaction.transaction_date == obj.transaction_date,
                Transaction.amount == obj.amount,
                Transaction.description == obj.description
            )).scalar()
            # If transaction does not exist, add it to the list of new transactions
            if not is_existing:
                # Create the transaction object
                new_transaction = Transaction(
                    user_id=user_id,
                    category_id=2 if obj.transaction_type.lower() == "income" else 1,
                    subcategory_id=6 if obj.transaction_type.lower() == "income" else 1,
                    amount=obj.amount,
                    transaction_type=obj.transaction_type,
                    transaction_date=obj.transaction_date,
                    description=obj.description,
                    bank_id=1
                )
                add_transactions.append(new_transaction)

        # Only add the transactions that don't already exist
        if add_transactions:
            db.add_all(add_transactions)
            db.commit()

            # Update bank balances
            for transaction in add_transactions:
                bank = db.query(Bank).filter(
                    Bank.bank_id == transaction.bank_id).first()
                if bank:
                    if transaction.transaction_type.lower() == "income":
                        bank.total_balance += transaction.amount
                    elif transaction.transaction_type.lower() == "expense":
                        bank.total_balance -= transaction.amount

            db.commit()  # Commit balance updates

            return Response(status_code=status.HTTP_202_ACCEPTED, is_success=True, message="File Uploaded Successfully.", result=None)
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="No new transactions to upload.", result=None)
    # def upload_file(self, transactions: List[UploadTransaction], db: Session, user):
    #     user_id = user.get("sub")
    #     add_transactions = list(map(lambda obj: Transaction(user_id=user_id, category_id=2 if obj.transaction_type.lower() == "income" else 1, subcategory_id=6 if obj.transaction_type.lower() == "income" else 1,
    #                                                         amount=obj.amount, transaction_type=obj.transaction_type, transaction_date=obj.transaction_date,
    #                                                         description=obj.description, bank_id=1), transactions))

    #     db.add_all(add_transactions)
    #     db.commit()

    #     for transaction in add_transactions:
    #         bank = db.query(Bank).filter(
    #             Bank.bank_id == transaction.bank_id).first()
    #         if bank:
    #             # Increase for 'income', decrease for 'expense'
    #             if transaction.transaction_type.lower() == "income":
    #                 bank.total_balance += transaction.amount
    #             elif transaction.transaction_type.lower() == "expense":
    #                 bank.total_balance -= transaction.amount

    #     db.commit()  # Commit balance updates
    #     return Response(status_code=status.HTTP_202_ACCEPTED, is_success=True, message="File Uploaded Successfully.", result=None)


transaction_service = TransactionService()
