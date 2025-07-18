from flask import Blueprint, request, jsonify, g
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from services.client_service import (
    get_client_by_id, list_clients, create_client, update_client,
    find_client_by_phone, find_clients_by_full_name,
    get_orders_of_client
)

client_router = Blueprint("client_router", __name__)

#====================GET METHODS====================#

@client_router.get("/")
def list_clients_route():
    db = g.db
    clients = list_clients(db)
    return jsonify([c.to_dict() for c in clients]), HTTPStatus.OK

@client_router.get("/<int:client_id>")
def get_client_by_id_route(client_id):
    db = g.db
    client = get_client_by_id(db, client_id)
    return jsonify(client.to_dict()), HTTPStatus.OK

@client_router.get("/phone/<string:phone>")
def find_client_by_phone_route(phone):
    db = g.db
    client = find_client_by_phone(db, phone)
    return jsonify(client.to_dict()), HTTPStatus.OK

@client_router.get("/name")
def find_client_by_full_name_route():
    db = g.db
    first_name = request.args.get("first_name", "").strip()
    last_name = request.args.get("last_name", "").strip()

    if not first_name or not last_name:
        raise BadRequest("first_name and last_name are required and cannot be empty.")

    clients = find_clients_by_full_name(db, first_name, last_name)
    return jsonify([client.to_dict() for client in clients]), HTTPStatus.OK

@client_router.get("/<int:client_id>/orders")
def get_orders_of_client_route(client_id):
    db = g.db
    orders = get_orders_of_client(db, client_id)
    return jsonify([o.to_dict() for o in orders]), HTTPStatus.OK

#====================POST METHOD====================#

@client_router.post("/")
def create_client_route():
    db = g.db
    data = request.get_json()
    try:
        client = create_client(db, data)
        return jsonify(client.to_dict()), HTTPStatus.CREATED
    except (KeyError, ValueError) as e:
        raise BadRequest(str(e))

#====================PATCH METHOD====================#

@client_router.patch("/<int:client_id>")
def update_client_route(client_id):
    db = g.db
    updates = request.get_json()
    if not updates:
        raise BadRequest("No update data provided")
    updated = update_client(db, client_id, updates)
    return jsonify(updated.to_dict()), HTTPStatus.OK
