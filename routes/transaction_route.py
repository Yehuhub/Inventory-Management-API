from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.transaction_service import get_transaction_by_id, get_transactions_by_user_id, get_transactions_with_filters, create_transaction
from services.user_service import get_user_by_id
from services.branch_service import get_branch_by_id
from datetime import datetime
from models.Transaction import TRANSACTION_TYPES

transaction_router = Blueprint("transaction_route", __name__)

#====================GET METHODS====================#

# get list of transaction
# optional filtering using query params:
#   start_date/end_date to filter transactions between dates
#   transaction_type for 'receive'/'send' transactions
#   branch_id to find only transactions in this branch
@transaction_router.get("/")
def get_transactions():
    db = g.db

    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    transaction_type = request.args.get("transaction_type")
    branch_id = request.args.get("branch_id")

    start_date = None
    end_date = None
    date_format = "%d-%m-%Y"

    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, date_format).date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, date_format).date()
    except ValueError:
        raise BadRequest("Invalid date format")
    
    if transaction_type:
        transaction_type = transaction_type.lower()
        if transaction_type not in TRANSACTION_TYPES:
            raise BadRequest(f"Invalid transaction type: {transaction_type}")

    if branch_id:
        if not branch_id.isdigit():
            raise BadRequest("branch_id must be an integer")
        branch_id = int(branch_id)
        if branch_id < 1:
            raise BadRequest("branch_id must be a positive integer")
        get_branch_by_id(db, branch_id)  # raises NotFound if branch is not found

    transactions = get_transactions_with_filters(db, start_date, end_date, transaction_type, branch_id)
    return jsonify([transaction.to_dict() for transaction in transactions])

# get specific transaction by id
@transaction_router.get("/<int:transaction_id>")
def get_transaction_by_id_route(transaction_id):
    db = g.db

    transaction = get_transaction_by_id(db, transaction_id)
    return jsonify(transaction.to_dict()), HTTPStatus.OK


# get all transactions made by a user
@transaction_router.get("/user/<int:user_id>")
def get_transaction_by_user(user_id):
    db = g.db
    get_user_by_id(db, user_id)  # raises not found if user_id doesnt exists

    transactions = get_transactions_by_user_id(db, user_id)
    return jsonify([transaction.to_dict() for transaction in transactions])


#====================POST METHODS====================#

# create a transaction, body json format:
# all fields are required
# {
#     "quantity": int,
#     "transaction_type": "send"/"receive"
#     "user_id": int,
#     "item_id": int,
#     "branch_id": int
# }
@transaction_router.post("/")
def create_new_transaction():
    db = g.db
    data = request.get_json()

    required_fields = ["quantity", "transaction_type", "user_id", "item_id", "branch_id"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        raise BadRequest(f"Missing required fields: {', '.join(missing)}")

    transaction_type = data["transaction_type"]
    description = data.get("description", "")
    branch_id = validate_positive_int(data["branch_id"], "branch_id")
    quantity = validate_positive_int(data["quantity"], "quantity")
    user_id = validate_positive_int(data["user_id"], "user_id")
    item_id = validate_positive_int(data["item_id"], "item_id")

    if transaction_type.lower() not in TRANSACTION_TYPES:
        raise BadRequest(f"Invalid transaction type: {transaction_type}")

    transaction = create_transaction(
        db,
        {
            "quantity": quantity,
            "transaction_type": transaction_type.lower(),
            "user_id": user_id,
            "item_id": item_id,
            "branch_id": branch_id,
            "description": description
        }
    )

    return jsonify(transaction.to_dict()), HTTPStatus.CREATED


def validate_positive_int(value, field_name):
    if not isinstance(value, int) or value <= 0:
        raise BadRequest(f"{field_name} must be a positive integer")
    return value
