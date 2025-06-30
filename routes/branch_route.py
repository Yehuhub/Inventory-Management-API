from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.branch_service import (
    get_branch_by_id, get_all_branches, get_manager_by_branch_id,
    get_users_by_branch_id, get_transactions_by_branch_id,
    get_item_stocks_by_branch_id, create_branch, delete_branch,
    assign_manager_to_branch, remove_manager_from_branch
)
from models import Branch

branch_router = Blueprint("branch_router", __name__)


# ====================GET METHODS====================#

@branch_router.get("/")
def get_all_branches_route():
    db = g.db
    branches = get_all_branches(db)
    return jsonify([branch.to_dict() for branch in branches]), HTTPStatus.OK


@branch_router.get("/<int:branch_id>")
def get_branch_by_id_route(branch_id):
    db = g.db
    branch = get_branch_by_id(db, branch_id)
    return jsonify(branch.to_dict()), HTTPStatus.OK


@branch_router.get("/<int:branch_id>/manager")
def get_branch_manager(branch_id):
    db = g.db
    manager = get_manager_by_branch_id(db, branch_id)
    return jsonify(manager.to_dict()), HTTPStatus.OK


@branch_router.get("/<int:branch_id>/users")
def get_branch_users(branch_id):
    db = g.db
    users = get_users_by_branch_id(db, branch_id)
    return jsonify([user.to_dict() for user in users]), HTTPStatus.OK


@branch_router.get("/<int:branch_id>/transactions")
def get_branch_transactions(branch_id):
    db = g.db
    transactions = get_transactions_by_branch_id(db, branch_id)

    return jsonify([transaction.to_dict() for transaction in transactions]), HTTPStatus.OK


@branch_router.get("/<int:branch_id>/item-stocks")
def get_branch_item_stocks(branch_id):
    db = g.db
    item_stocks = get_item_stocks_by_branch_id(db, branch_id)
    return jsonify([stock.to_dict() for stock in item_stocks]), HTTPStatus.OK


# ====================POST METHODS====================#

@branch_router.post("/")
def create_branch_route():
    db = g.db
    data = request.get_json()

    try:
        branch = Branch(
            name=data["name"],
            address=data["address"],
            phone_number=data["phone_number"]
        )
        created = create_branch(db, branch)
        return jsonify(created.to_dict()), HTTPStatus.CREATED

    except KeyError as e:
        raise BadRequest(f"Missing field: {str(e)}")
    except ValueError as e:
        raise BadRequest(str(e))


# ====================DELETE METHODS====================#

@branch_router.delete("/<int:branch_id>")
def delete_branch_route(branch_id):
    print("in delete")
    db = g.db
    delete_branch(db, branch_id)
    return jsonify({"message": f"Branch {branch_id} deleted"}), HTTPStatus.OK


# ====================PATCH METHODS====================#

@branch_router.patch("/<int:branch_id>/assign-manager")
def assign_manager(branch_id):
    db = g.db
    data = request.get_json()
    manager_id = data.get("manager_id")

    if not manager_id or not isinstance(manager_id, int):
        raise BadRequest("Missing or invalid manager_id")

    updated_branch = assign_manager_to_branch(db, branch_id, manager_id)
    return jsonify(updated_branch.to_dict()), HTTPStatus.OK


@branch_router.patch("/<int:branch_id>/remove-manager")
def remove_manager(branch_id):
    db = g.db
    updated_branch = remove_manager_from_branch(db, branch_id)
    return jsonify(updated_branch.to_dict()), HTTPStatus.OK
