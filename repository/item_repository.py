from repository.base_repository import BaseRepository
from models import Item
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class ItemRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Item)

    #Retrieves item category by item ID
    def get_category_by_item_id(self, item_id):
        stmt = select(Item).where(Item.id == item_id).options(selectinload(Item.category))
        item = self.db.execute(stmt).scalars().first()
        return item.category if item else None
    
    # Retrieves item stocks by item ID
    def get_item_stocks_by_item_id(self, item_id):
        stmt = select(Item).where(Item.id == item_id).options(selectinload(Item.item_stocks))
        item = self.db.execute(stmt).scalars().first()
        return item.item_stocks if item else None
    
    
    
    # Retrieves prices associated with an item by item ID
    def get_prices_by_item_id(self, item_id):
        stmt = select(Item).where(Item.id == item_id).options(selectinload(Item.prices))
        item = self.db.execute(stmt).scalars().first()
        return item.prices if item else None
    
    # Retrieves the price of an item based on its ID and the amount purchased
    def get_item_price_by_id_and_amount(self, item_id, amount):
        stmt = select(Item).where(Item.id == item_id).options(selectinload(Item.prices))
        item = self.db.execute(stmt).scalars().first()

        if not item:
            return None

        sorted_prices = sorted(item.prices, key=lambda price: price.min_quantity)

        current_price = 0
        if item:
            for price in sorted_prices:
                if amount >= price.min_quantity:
                    current_price = price.price_per_unit
                else:
                    break

        return current_price if current_price > 0 else None