from repository.order_repository import OrderRepository
from repository.order_item_repository import OrderItemRepository
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from services.item_service import get_item_price_by_id_and_amount, get_item_by_id
from services.order_item_service import create_order_item
from services.user_service import get_user_by_id
from services.client_service import get_client_by_id
from datetime import date, timedelta
from models.Order import ORDER_STATUS, Order
from models.OrderItem import OrderItem
from sqlalchemy.exc import SQLAlchemyError


def get_order_by_id(db, order_id: int):
    order_repository = OrderRepository(db)
    order = order_repository.get_by_id(order_id)
    if not order:
        raise BadRequest("Order not found")
    return order

def list_orders(db):
    order_repository = OrderRepository(db)
    return order_repository.list_all()


# creates the order based on the new order format, rollsback the db if fails at any point
def create_order(db, order_data: dict):

    try:
        user = get_user_by_id(order_data["user_id"])
        client = get_client_by_id(order_data["client_id"])
        
        new_order = Order(
            user_id=user.id,
            client_id=client.id,
            status="pending",
            delivery_date=date.today() + timedelta(days=14),
            price=0.0
            )
        db.add(new_order)
        db.flush()

        total_price = 0.0
        for item in order_data["order_items"]:
            item_id = item["item_id"]
            quantity = item["quantity"]

            get_item_by_id(item_id) # will raise not found if doesnt exists

            item_price = get_item_price_by_id_and_amount(item_id=item_id, amount=quantity)
            order_item_price = round(item_price * quantity,2)
            total_price += order_item_price

            new_order_item = OrderItem(
                order_id=new_order.id,
                item_id=item_id,
                quantity=quantity,
                price=order_item_price
            )
            db.add(new_order_item)

        new_order.total_price = round(total_price, 2)

        db.commit()
        db.refresh(new_order)
        return new_order

    except (BadRequest, NotFound) as e:
        db.rollback()
        raise e
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def update_order(db, order_id: int, updates: dict):
    order_repository = OrderRepository(db)
    order = order_repository.get_by_id(order_id)
    if not order:
        raise BadRequest("Order not found")
    return order_repository.update(order, updates)

def delete_order(db, order_id: int):
    order_repository = OrderRepository(db)
    order = order_repository.get_by_id(order_id)
    if not order:
        raise BadRequest("Order not found")
    try:
        order_repository.delete(order)
        return order
    except Exception:
        raise InternalServerError("Error deleting order")

def get_orders_by_client_id(db, client_id: int):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_client_id(client_id)
    return orders

def get_orders_by_user_id(db, user_id: int):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_user_id(user_id)
    return orders

def get_orders_by_status(db, status: str):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_status(status)
    return orders

def get_orders_by_delivery_date(db, delivery_date: date):
    order_repository = OrderRepository(db)
    orders = order_repository.get_orders_by_delivery_date(delivery_date)
    return orders

def get_order_items(db, order_id: int):
    order_repository = OrderRepository(db)
    items = order_repository.get_order_with_items(order_id)
    return items

def get_orders_with_filters(db, start_date = None, end_date = None, date_field="createdAt", status=None):
    order_repository = OrderRepository(db)

    if date_field not in ["createdAt", "updatedAt"]:
        raise BadRequest("Invalid date field. use createdAt or updatedAt")
    
    if status is not None and status not in ORDER_STATUS:
        raise BadRequest(f"Invalid status filter {','.join(ORDER_STATUS)}")

    orders = order_repository.get_orders_with_filters(start_date, end_date, date_field, status)

    if not orders:
        raise NotFound("Could not find orders with specified filters")
    return orders
