from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.category_service import (
    get_all_categories, create_category, get_items_by_category_id, get_items_by_category_name,
    get_category_by_name, delete_category as delete_category_by_id
)
from models import Category

category_router = Blueprint("category_router", __name__)

#====================GET METHODS====================#

# List all the categories
@category_router.get("/")
def get_all_categories_route():
    db = g.db
    categories = get_all_categories(db)
    return jsonify([cat.to_dict() for cat in categories]), HTTPStatus.OK

# List All items with this category id
@category_router.get("/<int:category_id>/items")
def get_items_by_category_id_route(category_id):
    db = g.db
    items = get_items_by_category_id(db, category_id)
    return jsonify([item.to_dict() for item in items]), HTTPStatus.OK

# List all items with this category id
@category_router.get("/<category_name>/items")
def get_items_by_category_name_route(category_name):
    db = g.db
    items = get_items_by_category_name(db, category_name)
    return jsonify([item.to_dict() for item in items]), HTTPStatus.OK

#====================POST METHODS====================#

# create a new category
@category_router.post("/")
def create_category_route():
    db = g.db
    data = request.get_json()

    try:
        category = Category(name=data["name"])
        created = create_category(db, category)
        return jsonify(created.to_dict()), HTTPStatus.CREATED
    except KeyError:
        raise BadRequest("Missing 'name' field")
    except ValueError as e:
        raise BadRequest(str(e))

#====================DELETE METHODS====================#

# delete a category by id
@category_router.delete("/<int:category_id>")
def delete_category_by_id_route(category_id):
    db = g.db
    delete_category_by_id(db, category_id)
    return jsonify({"message": f"Category {category_id} deleted"}), HTTPStatus.OK


# delete category by name
@category_router.delete("/name/<string:category_name>")
def delete_category_by_name_route(category_name):
    db = g.db
    category = get_category_by_name(db, category_name)
    delete_category_by_id(db, category.id)
    return jsonify({"message": f"Category '{category_name}' deleted"}), HTTPStatus.OK
