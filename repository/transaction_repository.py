from repository.base_repository import BaseRepository
from models import Transaction
from sqlalchemy import select
from datetime import datetime, date

class TransactionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Transaction)

    # Get all transactions by user
    def get_transactions_by_user_id(self, user_id: int):
        stmt = select(Transaction).where(Transaction.user_id == user_id)
        return self.db.execute(stmt).scalars().all()

    # Get all transactions by item
    def get_transactions_by_item_id(self, item_id: int):
        stmt = select(Transaction).where(Transaction.item_id == item_id)
        return self.db.execute(stmt).scalars().all()

    # Get all transactions by branch
    def get_transactions_by_branch_id(self, branch_id: int):
        stmt = select(Transaction).where(Transaction.branch_id == branch_id)
        return self.db.execute(stmt).scalars().all()

    # Get all transactions created on a specific date
    def get_transactions_by_date(self, specific_date: date):
        stmt = select(Transaction).where(
            Transaction.created_at.between(
                datetime.combine(specific_date, datetime.min.time()),
                datetime.combine(specific_date, datetime.max.time())
            )
        )
        return self.db.execute(stmt).scalars().all()
    # Get all transactions for a specific user on a specific date
    def get_transactions_by_date_and_user(self, specific_date: date, user_id: int):
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.created_at.between(
                datetime.combine(specific_date, datetime.min.time()),
                datetime.combine(specific_date, datetime.max.time())
            )
        )
        return self.db.execute(stmt).scalars().all()

    # Get all transactions for a specific branch on a specific date
    def get_transactions_by_date_and_branch(self, specific_date: date, branch_id: int):
        stmt = select(Transaction).where(
            Transaction.branch_id == branch_id,
            Transaction.created_at.between(
                datetime.combine(specific_date, datetime.min.time()),
                datetime.combine(specific_date, datetime.max.time())
            )
        )
        return self.db.execute(stmt).scalars().all()

    # Get all transactions for a specific item on a specific date
    def get_transactions_by_date_and_item(self, specific_date: date, item_id: int):
        stmt = select(Transaction).where(
            Transaction.item_id == item_id,
            Transaction.created_at.between(
                datetime.combine(specific_date, datetime.min.time()),
                datetime.combine(specific_date, datetime.max.time())
            )
        )
        return self.db.execute(stmt).scalars().all()

    def get_transactions_with_filters(self, start_date = None, end_date = None, transaction_type = None, branch_id=None):
        stmt = None
        transaction_date = getattr(Transaction, "created_at")

        filters = []
        if start_date:
            filters.append(transaction_date >= start_date)
        if end_date:
            filters.append(transaction_date <= end_date)
        if transaction_type:
            filters.append(Transaction.transaction_type == transaction_type)
        if branch_id:
            filters.append(Transaction.branch_id == branch_id)

        if filters:
            stmt = select(Transaction).where(*filters)
        else:
            return self.list_all()
        
        stmt = stmt.order_by(transaction_date.desc())
        return self.db.execute(stmt).scalars().all