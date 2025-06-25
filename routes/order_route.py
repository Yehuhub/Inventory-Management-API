from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.order_service import get_order_by_id, get_orders_with_filters, get_order_items, create_order
from services.user_service import get_orders_by_user_id
from services.client_service import get_orders_of_client
from datetime import datetime


order_router = Blueprint("order_router", __name__)

#==========GET METHODS==========#

# get orders, can filter by start-end dates, and if we query dates by update date or created date, and order status
@order_router.get("/")
def list_all_orders():

    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    filter_by = request.args.get("filter_by", "created").lower()
    status = request.args.get("status")

    date_field = "updatedAt" if filter_by == "updated" else "createdAt"

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


    db = g.db
    orders = get_orders_with_filters(db, start_date, end_date, date_field, status)
    return jsonify([order.to_dict() for order in orders]), HTTPStatus.OK

# get an order by order_id
@order_router.get("/<int:order_id>")
def get_order_by_order_id(order_id):
    db = g.db
    order = get_order_by_id(db, order_id)
    return jsonify(order.to_dict()), HTTPStatus.OK

# get an order by order_id
@order_router.get("/user/<int:user_id>")
def get_order_by_order_id(user_id):
    db = g.db
    orders = get_orders_by_user_id(db, user_id)
    return jsonify(order.to_dict() for order in orders), HTTPStatus.OK

# get all orders for client
@order_router.get("/client/<int:client_id>")
def get_order_by_order_id(client_id):
    db = g.db
    orders = get_orders_of_client(db, client_id)
    return jsonify(order.to_dict() for order in orders), HTTPStatus.OK

# get the order items for a specific order id
@order_router.get("/order-items/<int:order_id>")
def get_order_items_by_order_id(order_id):
    db = g.db
    order_items = get_order_items(db, order_id)
    return jsonify(order_item.to_dict() for order_item in order_items), HTTPStatus.OK



#==========POST METHODS==========#

@order_router.post("/")
def create_a_new_order():
    db = g.db
    data = request.get_json()

    REQUIRED_FIELDS = ["order_items", "user_id", "client_id"]

    # validate all required fields are present
    for field in REQUIRED_FIELDS:
        if field not in data:
            raise BadRequest(f"Missing required field {field}")
        
    # validates order_items is a list
    order_items = data["order_items"]
    if not isinstance(order_items, list) or not order_items:
        raise BadRequest("order_items must be a non empty list")
    
    # validate id's and quantities are integers and quantity is positive
    for i, item in enumerate(order_items):
        if "item_id" not in item or "quantity" not in item:
            raise BadRequest(f"Each order item must have 'item_id' and 'quantity' (issue at index {i})")
        if not isinstance(item["item_id"], int) or not isinstance(item["quantity"], int):
            raise BadRequest(f"'item_id' and 'quantity' must be integers (index {i})")
        if item["quantity"] <= 0:
            raise BadRequest(f"Quantity must be greater than 0 (index {i})")
        
    order = create_order(db, {
        "order_items":order_items,
        "client_id": data["client_id"],
        "user_id": data["user_id"],
    })

    return jsonify(order.to_dict()), HTTPStatus.CREATED