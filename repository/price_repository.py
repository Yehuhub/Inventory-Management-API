from repository.base_repository import BaseRepository
from models import Price
from sqlalchemy import select

class PriceRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Price)

    # Get all prices for a specific item
    def get_prices_by_item_id(self, item_id: int):
        stmt = select(Price).where(Price.item_id == item_id)
        return self.db.execute(stmt).scalars().all()

    # Get the best price for a given item and quantity (based on min_quantity rule)
    def get_best_price_for_quantity(self, item_id: int, quantity: int):
        stmt = (
            select(Price)
            .where(Price.item_id == item_id, Price.min_quantity <= quantity)
            .order_by(Price.min_quantity.desc())  # More specific (higher min_quantity) first
        )
        return self.db.execute(stmt).scalars().first()
