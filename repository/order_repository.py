from repository.base_repository import BaseRepository
from models import Order
from sqlalchemy import select, column
from datetime import date


class OrderRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Order)

    # Get all orders by client_id
    def get_orders_by_client_id(self, client_id: int):
        stmt = select(Order).where(Order.client_id == client_id)
        return self.db.execute(stmt).scalars().all()

    # Get all orders by user_id
    def get_orders_by_user_id(self, user_id: int):
        stmt = select(Order).where(Order.user_id == user_id)
        return self.db.execute(stmt).scalars().all()

    # Get orders by status (e.g., 'pending' or 'delivered')
    def get_orders_by_status(self, status: str):
        stmt = select(Order).where(Order.status == status.strip().lower())
        return self.db.execute(stmt).scalars().all()

    # Get all orders with a specific delivery date
    def get_orders_by_delivery_date(self, delivery: date):
        stmt = select(Order).where(Order.delivery_date == delivery)
        return self.db.execute(stmt).scalars().all()

    # Get an order including its items
    def get_order_with_items(self, order_id: int):
        stmt = select(Order).where(Order.id == order_id)
        result = self.db.execute(stmt).scalars().first()
        return result.items if result else None

    # Get orders between specified dates
    def get_orders_with_filters(self, start_date = None, end_date = None, date_field="createdAt", status = None):

        stmt = None
        order_date = getattr(Order, date_field)

        filters = []
        if start_date:
            filters.append(order_date >= start_date)
        if end_date:
            filters.append(order_date <= end_date)
        if status:
            filters.append(Order.status == status)

        if filters:
            stmt = select(Order).where(*filters)
        else:
            return self.list_all()
        
        stmt = stmt.order_by(order_date.desc())
        return self.db.execute(stmt).scalars().all()
        
