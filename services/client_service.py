from repository.client_repository import ClientRepository
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest

def get_client_by_id(db, client_id: int):
    client_repository = ClientRepository(db)
    client = client_repository.get_by_id(client_id)
    if not client:
        raise BadRequest("Client not found")
    return client

def list_clients(db):
    client_repository = ClientRepository(db)
    return client_repository.list_all()

def create_client(db, client_data: dict):
    client_repository = ClientRepository(db)
    client = client_repository.model(**client_data)
    return client_repository.create(client)

def update_client(db, client_id: int, updates: dict):
    client_repository = ClientRepository(db)
    client = client_repository.get_by_id(client_id)
    if not client:
        raise BadRequest("Client not found")
    return client_repository.update(client, updates)

def delete_client(db, client_id: int):
    client_repository = ClientRepository(db)
    client = client_repository.get_by_id(client_id)
    if not client:
        raise BadRequest("Client not found")
    try:
        client_repository.delete(client)
        return client
    except Exception:
        raise InternalServerError("Error deleting client")

def find_client_by_full_name(db, first_name: str, last_name: str):
    client_repository = ClientRepository(db)
    client = client_repository.find_by_full_name(first_name, last_name)
    if not client:
        raise BadRequest("Client not found")
    return client

def find_client_by_phone(db, phone: str):
    client_repository = ClientRepository(db)
    client = client_repository.find_by_phone(phone)
    if not client:
        raise BadRequest("Client not found")
    return client

def get_orders_of_client(db, client_id: int):
    client_repository = ClientRepository(db)
    client = client_repository.get_by_id(client_id)
    if not client:
        raise BadRequest("Client not found")
    return client_repository.get_orders_by_client_id(client_id)