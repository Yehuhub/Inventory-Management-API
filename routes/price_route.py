from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest
from services.price_service import create_price, update_price
from data.ORMSetup import get_db

price_router = Blueprint("price_route", __name__)

# Create a new price
@price_router.route("/", methods=["POST"])
def create_new_price():
    db = get_db()
    data = request.get_json()

    required_fields = ["item_id", "min_quantity", "price_per_unit"]
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")

    try:
        price = create_price(db, data)
        return jsonify(price.to_dict()), 201
    except SQLAlchemyError as e:
        db.rollback()
        raise BadRequest(str(e))


# Update an existing price
@price_router.route("/<int:price_id>", methods=["PATCH"])
def update_existing_price(price_id):
    db = get_db()
    data = request.get_json()

    if not data:
        raise BadRequest("No update fields provided")

    try:
        updated_price = update_price(db, price_id, data)
        return jsonify(updated_price.to_dict())
    except SQLAlchemyError as e:
        db.rollback()
        raise BadRequest(str(e))
