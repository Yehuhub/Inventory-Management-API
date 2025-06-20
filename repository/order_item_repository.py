from repository.base_repository import BaseRepository
from models import Client, Order, OrderItem
from sqlalchemy import select

class OrderItemRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, OrderItem)

    # Get all items in a specific order
    def get_items_by_order_id(self, order_id: int):
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        return self.db.execute(stmt).scalars().all()

    # Get all order items for a specific item_id (to see where it's used)
    def get_order_items_by_item_id(self, item_id: int):
        stmt = select(OrderItem).where(OrderItem.item_id == item_id)
        return self.db.execute(stmt).scalars().all()

    # Get phone numer of the client that made the order of this item
    def get_client_phone_by_order_item_id(self, order_item_id: int):
        stmt = (
            select(Client.phone_number)
            .join(Order, Client.id == Order.client_id)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .where(OrderItem.id == order_item_id)
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        return result