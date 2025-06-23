from datetime import date

from repository.transaction_repository import TransactionRepository
from werkzeug.exceptions import NotFound, InternalServerError

def get_transaction_by_id(db, transaction_id: int):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.get_by_id(transaction_id)
    if not transaction:
        raise NotFound("Transaction not found")
    return transaction

def list_transactions(db):
    transaction_repository = TransactionRepository(db)
    return transaction_repository.list_all()

def create_transaction(db, transaction_data: dict):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.model(**transaction_data)
    return transaction_repository.create(transaction)

def update_transaction(db, transaction_id: int, updates: dict):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.get_by_id(transaction_id)
    if not transaction:
        raise NotFound("Transaction not found")
    return transaction_repository.update(transaction, updates)

def delete_transaction(db, transaction_id: int):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.get_by_id(transaction_id)
    if not transaction:
        raise NotFound("Transaction not found")
    try:
        transaction_repository.delete(transaction)
        return transaction
    except Exception:
        raise InternalServerError("Error deleting transaction")

def get_transactions_by_user_id(db, user_id: int):
    transaction_repository = TransactionRepository(db)
    transactions = transaction_repository.get_transactions_by_user_id(user_id)
    if not transactions:
        raise NotFound(f"No transactions found for user_id={user_id}")
    return transactions

def get_transactions_by_date(db, specific_date: date):
    transaction_repository = TransactionRepository(db)
    transactions = transaction_repository.get_transactions_by_date(specific_date)
    if not transactions:
        raise NotFound(f"No transactions found on {specific_date}")
    return transactions

def get_transactions_by_item_id(db, item_id: int):
    transaction_repository = TransactionRepository(db)
    transactions = transaction_repository.get_transactions_by_item_id(item_id)
    if not transactions:
        raise NotFound(f"No transactions found for item_id= {item_id}")
    return transactions


def get_transactions_by_branch_id(db, branch_id: int):
    transaction_repository = TransactionRepository(db)
    transactions = transaction_repository.get_transactions_by_branch_id(branch_id)
    if not transactions:
        raise NotFound(f"No transactions found for branch_id= {branch_id}")
    return transactions


def get_transactions_by_date_and_user(db, specific_date: date, user_id: int):
    transaction_repository = TransactionRepository(db)
    return transaction_repository.get_transactions_by_date_and_user(specific_date, user_id)

def get_transactions_by_date_and_branch(db, specific_date: date, branch_id: int):
    transaction_repository = TransactionRepository(db)
    return transaction_repository.get_transactions_by_date_and_branch(specific_date, branch_id)

def get_transaction_by_date_and_item(db, specific_date: date, item_id: int):
    transaction_repository = TransactionRepository(db)
    return transaction_repository.get_transactions_by_date_and_item(specific_date, item_id)