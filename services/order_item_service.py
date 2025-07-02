from repository.order_item_repository import OrderItemRepository
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest

def get_order_item_by_id(db, order_item_id: int):
    order_item_repository = OrderItemRepository(db)
    order_item = order_item_repository.get_by_id(order_item_id)
    if not order_item:
        raise BadRequest("Order item not found")
    return order_item

def list_order_item(db):
    order_item_repository = OrderItemRepository(db)
    return order_item_repository.list_all()

def create_order_item(db,order_item_data: dict):
    order_item_repository = OrderItemRepository(db)
    order_item = order_item_repository.model(**order_item_data)
    return order_item_repository.create(order_item)

def update_order_item(db, order_item_id: int, updates: dict):
    order_item_repository = OrderItemRepository(db)
    order_item = order_item_repository.get_by_id(order_item_id)
    if not order_item:
        raise BadRequest("Order Item not found")
    return order_item_repository.update(order_item, updates)

def delete_order_item(db,order_item_id: int):
    order_item_repository = OrderItemRepository(db)
    order_item = order_item_repository.get_by_id(order_item_id)
    if not order_item:
        raise BadRequest("Order Item not found")
    try:
        order_item_repository.delete(order_item)
        return order_item
    except Exception:
        raise InternalServerError("Error deleting order item")

def get_items_by_order_id(db, order_id: int):
    order_item_repository = OrderItemRepository(db)
    items = order_item_repository.get_items_by_order_id(order_id)
    return items

def get_order_items_by_item_id(db, item_id: int):
    order_item_repository = OrderItemRepository(db)
    order_items = order_item_repository.get_order_items_by_item_id(item_id)
    return order_items

def get_client_phone_by_order_item_id(db, order_item_id: int):
    order_item_repository = OrderItemRepository(db)
    phone = order_item_repository.get_client_phone_by_order_item_id(order_item_id)
    if not phone:
        raise BadRequest(f"No client phone found for order_item_id={order_item_id}")
    return phone