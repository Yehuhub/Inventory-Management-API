from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.user_service import get_user_by_phone
from utils.auth import create_token

auth_router = Blueprint("auth_router", __name__)


@auth_router.post("/login")
def login():
    db = g.db
    data = request.get_json()
    phone_number = data.get("phone_number") if data else None
    if not phone_number:
        raise BadRequest("Missing phone_number")

    user = get_user_by_phone(db, phone_number)
    token = create_token(user.id, user.role)
    return jsonify({"token": token, "user_id": user.id, "role": user.role}), HTTPStatus.OK
