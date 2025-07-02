from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from models import User
from services.user_service import (
    get_user_by_id,
    get_all_users,
    create_user,
    delete_user,
    update_user,
)

user_router = Blueprint("user_router", __name__)

#====================GET METHODS====================#

# Get all users
@user_router.get("/")
def get_all_users_route():
    db = g.db
    users = get_all_users(db)
    return jsonify([user.to_dict() for user in users]), HTTPStatus.OK

# Get a user by ID
@user_router.get("/<int:user_id>")
def get_user_by_id_route(user_id):
    db = g.db
    user = get_user_by_id(db, user_id)
    return jsonify(user.to_dict()), HTTPStatus.OK

#====================POST METHODS====================#

# Create a new user
@user_router.post("/")
def create_new_user_route():
    db = g.db
    data = request.get_json()

    try:
        user = User(
            first_name = data["first_name"],
            last_name = data["last_name"],
            phone_number = data["phone_number"],
            role=data["role"],
            branch_id=data.get("branch_id")
        )
        created_user = create_user(db, user)
        return jsonify(created_user.to_dict()), HTTPStatus.CREATED
    except KeyError as e:
        raise BadRequest(f"Missing field: {str(e)}")
    except Exception as e:
        raise BadRequest(str(e))

#====================DELETE METHODS====================#

# Delete a user by ID
@user_router.delete("/<int:user_id>")
def delete_user_route(user_id):
    db = g.db
    delete_user(db, user_id)
    return jsonify({"message": "User deleted"}), HTTPStatus.OK

#====================PATCH METHODS====================#

# Update some fields of a user
@user_router.patch("/<int:user_id>")
def patch_user_route(user_id):
    db = g.db
    data = request.get_json()

    if not data:
        raise BadRequest("No update data provided")

    updated_user = update_user(db, user_id, data)
    return jsonify(updated_user.to_dict()), HTTPStatus.OK
