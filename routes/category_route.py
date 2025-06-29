from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.category_service import (
    get_all_categories, create_category, delete_category,
    get_category_by_name, delete_category as delete_category_by_id
)
from models import Category

category_router = Blueprint("category_router", __name__)

#====================GET METHODS====================#

@category_router.get("/")
def get_all_categories_route():
    db = g.db
    categories = get_all_categories(db)
    return jsonify([cat.to_dict() for cat in categories]), HTTPStatus.OK

#====================POST METHODS====================#

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

@category_router.delete("/<int:category_id>")
def delete_category_by_id_route(category_id):
    db = g.db
    delete_category_by_id(db, category_id)
    return jsonify({"message": f"Category {category_id} deleted"}), HTTPStatus.NO_CONTENT

@category_router.delete("/name/<string:category_name>")
def delete_category_by_name_route(category_name):
    db = g.db
    category = get_category_by_name(db, category_name)
    delete_category_by_id(db, category.id)
    return jsonify({"message": f"Category '{category_name}' deleted"}), HTTPStatus.NO_CONTENT
