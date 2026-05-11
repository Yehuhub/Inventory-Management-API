import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import g, jsonify
from http import HTTPStatus
from settings import JWT_SECRET

TOKEN_EXPIRY_HOURS = 1


def create_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])


def require_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.role != 'manager':
            return jsonify({"error": "Manager access required"}), HTTPStatus.FORBIDDEN
        return f(*args, **kwargs)
    return decorated
