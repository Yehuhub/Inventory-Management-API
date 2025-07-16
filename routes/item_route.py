from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from services.item_service import get_all_items, get_item_by_id, get_item_price_by_id_and_amount, create_item, get_item_prices_by_id, get_item_stocks_by_item_id
from services.branch_service import get_branch_by_id
from services.item_stock_service import get_item_stock_by_branch_and_item, update_item_stock
from services.price_service import update_price, get_price_by_id
from models import Item
from werkzeug.exceptions import BadRequest

item_router = Blueprint("item_router", __name__)

#====================GET METHODS====================#
# return a json list of all items
@item_router.get("/")
def get_items_route():
    db = g.db
    
    items = get_all_items(db)
    return jsonify([item.to_dict() for item in items]), HTTPStatus.OK

# return the requested object
@item_router.get("/<int:item_id>")
def get_item(item_id):
    db = g.db

    item = get_item_by_id(db, item_id)
    return jsonify(item.to_dict()), HTTPStatus.OK

# gets item_id and amount from query params and returns the cheapest price for this item
@item_router.get("/price")
def get_item_price():
    item_id = request.args.get("item_id", type=int)
    amount = request.args.get("amount", type=int)
    db = g.db

    if not amount or not item_id:
        raise BadRequest("Must provide item id and amount")
    
    if amount <= 0:
        raise BadRequest("Amount must be a positive number")
    
    item = get_item_by_id(db, int(item_id))
    price = get_item_price_by_id_and_amount(db, int(item_id), int(amount))
    return jsonify({"item_name": item.name,
                     "amount": amount,
                       "price_per_unit": price}), HTTPStatus.OK


# get all prices for an item
@item_router.get("/<int:item_id>/all-prices")
def get_all_item_prices(item_id):
    db = g.db
    
    prices = get_item_prices_by_id(db, item_id)
    return jsonify([price.to_dict() for price in prices]), HTTPStatus.OK

# gets all the stock for this item
@item_router.get("/<int:item_id>/all-stock")
def get_all_item_stock(item_id):
    db = g.db

    # will raise error if item doesnt exists
    item = get_item_by_id(db, item_id) 

    stocks = get_item_stocks_by_item_id(db, item_id)
    return jsonify([stock.to_dict() for stock in stocks]), HTTPStatus.OK
    

# get the stock for a specific item in a specific branch
@item_router.get("/<int:item_id>/stock/<int:branch_id>")
def get_stock_for_item_in_branch(item_id, branch_id):
    db = g.db
    item = get_item_by_id(item_id)
    branch = get_branch_by_id(branch_id)

    stock = get_item_stock_by_branch_and_item(db, item_id, branch_id)
    return jsonify(stock.to_dict()), HTTPStatus.OK

#====================POST METHODS====================#
# save a new item to the db
@item_router.post("/")
def create_new_item():
    db = g.db
    data = request.get_json()
    try:
        item = Item(
            name = data["name"],
            description = data.get("description"), # using .get as it can be null
            category_id = data["category_id"]
        )

        created_item = create_item(db, item)
        return jsonify(created_item.to_dict()), HTTPStatus.CREATED
    
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


#====================PATCH METHODS====================#

# patch method for updating stock quantity
@item_router.patch("/<int:item_id>/stock/<int:branch_id>")
def update_item_stock(item_id, branch_id):
    db = g.db
    data = request.get_json()

    quantity = data.get("quantity")
    if quantity is None or not isinstance(quantity, int) or quantity < 0:
        raise BadRequest("Invalid quantity")
    
    item_stock = get_item_stock_by_branch_and_item(db, item_id, branch_id)
    updated_stock = update_item_stock(db, item_stock.id, {"quantity": quantity})
    return jsonify(updated_stock.to_dict()), HTTPStatus.OK

# patch method, finds price matched by item_id and min_quantity, and updates quantity and price
@item_router.patch("/price/<int:price_id>")
def update_item_price_by_price_id(price_id):
    db = g.db
    data = request.get_json()

    updates = {}

    if "min_quantity" in data:
        min_qty = data["min_quantity"]
        if not isinstance(min_qty, int) or min_qty < 0:
            raise BadRequest("min_quantity must be a non-negative integer")
        updates["min_quantity"] = min_qty

    if "price_per_unit" in data:
        price = data["price_per_unit"]
        if not isinstance(price, (int, float)) or price <= 0:
            raise BadRequest("price_per_unit must be a positive number")
        updates["price_per_unit"] = price

    if not updates:
        raise BadRequest("No valid fields provided to update")

    old_price = get_price_by_id(db, price_id)
    updated_price = update_price(db, old_price.id, updates)

    return jsonify(updated_price.to_dict()), HTTPStatus.OK