from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.order_service import get_order_by_id, list_orders, get_orders_between_dates
from datetime import datetime


order_router = Blueprint("order_router", __name__)

#==========GET METHODS==========#

# get orders, can filter by start-end dates, and if we query dates by update date or created date
@order_router.get("/")
def list_all_orders():

    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    filter_by = request.args.get("filter_by", "created").lower()

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
    orders = get_orders_between_dates(db, start_date, end_date, date_field)
    return jsonify([order.to_dict() for order in orders]), HTTPStatus.OK

# get an order by order_id
@order_router.get("/<int:order_id>")
def get_order_by_order_id(order_id):
    db = g.db
    order = get_order_by_id(db, order_id)
    return jsonify(order.to_dict()), HTTPStatus.OK
