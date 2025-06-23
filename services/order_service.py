from repository.order_repository import OrderRepository
from werkzeug.exceptions import NotFound, InternalServerError
from datetime import date

def get_order_by_id(db, order_id: int):
    order_repository = OrderRepository(db)
    order = order_repository.get_by_id(order_id)
    if not order:
        raise NotFound("Order not found")
    return order

def list_orders(db):
    order_repository = OrderRepository(db)
    return order_repository.list_all()

def create_order(db, order_data: dict):
    order_repository = OrderRepository(db)
    order = order_repository.model(**order_data)
    return order_repository.create(order)

def update_order(db, order_id: int, updates: dict):
    order_repository = OrderRepository(db)
    order = order_repository.get_by_id(order_id)
    if not order:
        raise NotFound("Order not found")
    return order_repository.update(order, updates)

def delete_order(db, order_id: int):
    order_repository = OrderRepository(db)
    order = order_repository.get_by_id(order_id)
    if not order:
        raise NotFound("Order not found")
    try:
        order_repository.delete(order)
        return order
    except Exception:
        raise InternalServerError("Error deleting order")

def get_orders_by_client_id(db, client_id: int):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_client_id(client_id)
    if not orders:
        raise NotFound(f"No orders found for client_id={client_id}")
    return orders

def get_orders_by_user_id(db, user_id: int):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_user_id(user_id)
    if not orders:
        raise NotFound(f"No orders found for user_id={user_id}")
    return orders

def get_orders_by_status(db, status: str):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_status(status)
    if not orders:
        raise NotFound(f"No orders found with status={status}")
    return orders

def get_orders_by_delivery_date(db, delivery_date: date):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_delivery_date(delivery_date)
    if not orders:
        raise NotFound(f"No orders found for delivery_date={delivery_date}")
    return orders

def get_order_items(db, order_id: int):
    order_repository = OrderRepository(db)
    items = order_repository.get_order_with_items(order_id)
    if not items:
        raise NotFound(f"No items found for order_id={order_id}")
    return items
