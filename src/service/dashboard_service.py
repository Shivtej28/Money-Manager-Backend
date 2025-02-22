from datetime import date
from typing import List
from sqlalchemy.orm import Session
from ..models.data_model import Bank, Transaction
from ..scehmas.request_model import CategoryTypeEnum, DashboardBank, DashboardResponse, MainDashboardResponse, Response
from fastapi import status


class DashboardService:
    def __init__(self) -> None:
        pass

    def main_dashboard(self, start_date: date, end_date: date, db: Session, user):
        user_id = user.get("sub")
        all_transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id, Transaction.transaction_date >= start_date, Transaction.transaction_date <= end_date).all()
        if len(all_transactions) == 0:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please add Transactions", result=None)
        total_income = 0
        total_expense = 0

        for transaction in all_transactions:
            if transaction.transaction_type.lower() == CategoryTypeEnum.income.lower():
                total_income += transaction.amount
            elif transaction.transaction_type.lower() == CategoryTypeEnum.expense.lower():
                total_expense += transaction.amount

        total_savings = round(round(total_income, 2) -
                              round(total_expense, 2), 2)

        savings_percentage = round((total_savings/total_income)*100, 2)
        result = MainDashboardResponse(total_expense=total_expense, total_income=total_income,
                                       total_savings=total_savings, saving_percentage=str(savings_percentage) + "%")
        print(result)
        return Response(status_code=status.HTTP_200_OK, is_success=True, message="Main Dashboard Success", result=result)

    def get_all_details(self, db: Session, user):
        user_id = user.get("sub")
        # user_id = 1
        all_banks = db.query(Bank).filter(Bank.user_id == user_id).all()
        if len(all_banks) == 0:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please add Bank Deatils", result=None)
        total_balance = 0
        all_banks_response = []
        for bank in all_banks:
            total_balance += bank.total_balance
            response_bank = DashboardBank(bank_id=bank.bank_id, bank_name=bank.bank_name,
                                          bank_balance=bank.total_balance, account_type=bank.account_type)
            all_banks_response.append(response_bank)

        result = DashboardResponse(
            total_balance=total_balance, banks_details=all_banks_response)

        return Response(status_code=status.HTTP_200_OK, is_success=True, message="Income Expense Dashhboard Success", result=result)


dashboard_service = DashboardService()
