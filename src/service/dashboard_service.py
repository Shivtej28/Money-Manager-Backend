from sqlalchemy.orm import Session
from ..models.data_model import Transaction
from ..scehmas.request_model import CategoryTypeEnum, MainDashboardResponse, Response
from fastapi import status


class DashboardService:
    def __init__(self) -> None:
        pass

    def main_dashboard(self,db: Session, user):
        user_id = user.get("sub")
        all_transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id).all()
        if all_transactions is None:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, is_success=False, message="Please add Transactions", result=None)
        total_income = 0
        total_expense = 0

        for transaction in all_transactions:
            if transaction.transaction_type.lower() == CategoryTypeEnum.income.lower():
                total_income += transaction.amount
            elif transaction.transaction_type.lower() == CategoryTypeEnum.expense.lower():
                total_expense += transaction.amount

        total_savings = round(round(total_income, 2) - round(total_expense,2), 2)

        savings_percentage = round((total_savings/total_income)*100, 2)
        result = MainDashboardResponse(total_expense=total_expense, total_income=total_income,
                                       total_savings=total_savings, saving_percentage=str(savings_percentage) +"%")
        print(result)
        return Response(status_code=status.HTTP_200_OK, is_success=True, message="Main Dashboard Success", result=result)

dashboard_service = DashboardService()

            

        
