from datetime import date
from repository.transaction_repository import TransactionRepository
from services.user_service import get_user_by_id
from services.item_service import get_item_by_id
from services.branch_service import get_branch_by_id
from services.item_stock_service import get_item_stock_by_branch_and_item
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from models.Transaction import TRANSACTION_TYPES, Transaction
from models.ItemStock import ItemStock

# get specific transaction by id
def get_transaction_by_id(db, transaction_id: int):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.get_by_id(transaction_id)
    if not transaction:
        raise NotFound("Transaction not found")
    return transaction

# get all transactions
def list_transactions(db):
    transaction_repository = TransactionRepository(db)
    return transaction_repository.list_all()


# create transaction
# will create item_stock if receiving an item and stock not existing for it
def create_transaction(db, transaction_data: dict):
    try:
        # Validate and retrieve related entities
        user = get_user_by_id(db, transaction_data["user_id"])
        branch = get_branch_by_id(db, transaction_data["branch_id"])
        item = get_item_by_id(db, transaction_data["item_id"])
        quantity = transaction_data["quantity"]
        transaction_type = transaction_data["transaction_type"].lower()
        description = transaction_data.get("description", "")

        # Get the item stock (can be None)
        stock = get_item_stock_by_branch_and_item(db, item.id, branch.id)

        if transaction_type == "send":
            if not stock:
                raise BadRequest("Stock not found for this item in the selected branch")
            if stock.quantity < quantity:
                raise BadRequest(f"Not enough stock to send. Available: {stock.quantity}, requested: {quantity}")
            stock.quantity -= quantity

        elif transaction_type == "receive":
            if stock:
                stock.quantity += quantity
            else:
                # Create new stock if it doesn't exist
                stock = ItemStock(
                    quantity=quantity,
                    branch_id=branch.id,
                    item_id=item.id
                )
                db.add(stock)
        else:
            raise BadRequest("Invalid transaction type")

        # Create the transaction
        transaction = Transaction(
            quantity=quantity,
            transaction_type=transaction_type,
            user_id=user.id,
            item_id=item.id,
            branch_id=branch.id,
            description=description
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    except (NotFound, BadRequest) as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise BadRequest(f"Could not create transaction: {str(e)}")

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

def get_transactions_with_filters(db, start_date=None, end_date=None, transaction_type=None, branch_id=None):
    repo = TransactionRepository(db)

    transactions = repo.get_transactions_with_filters(start_date, end_date, transaction_type, branch_id)
    return transactions