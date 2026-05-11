import jwt
from functools import wraps
from flask import g, jsonify
from http import HTTPStatus
from settings import JWT_SECRET


def create_token(user_id: int, role: str) -> str:
    return jwt.encode({"user_id": user_id, "role": role}, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])


def require_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.role != 'manager':
            return jsonify({"error": "Manager access required"}), HTTPStatus.FORBIDDEN
        return f(*args, **kwargs)
    return decorated
