from repository.base_repository import BaseRepository
from models import ItemStock
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class ItemStockRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, ItemStock)

    # Retrieves all item stocks with their associated items
    def get_item_by_stock_id(self, stock_id):
        stmt = select(ItemStock).where(ItemStock.id == stock_id).options(selectinload(ItemStock.item))
        item_stock = self.db.execute(stmt).scalars().first()
        return item_stock.item if item_stock else None

    # Retrieves all itemstock associated with a specific item
    def get_item_stock_by_item_id(self, item_id):
        stmt = select(ItemStock).where(ItemStock.item_id == item_id)
        return self.db.execute(stmt).scalars().all()
    
    # Retrieves all item stocks associated with a specific branch
    def get_item_stock_by_branch_id(self, branch_id):
        stmt = select(ItemStock).where(ItemStock.branch_id == branch_id)
        return self.db.execute(stmt).scalars().all()
    
    # Retrieves item stock by branch and item ID
    # This method returns the stock for a specific item in a specific branch
    def get_item_stock_by_branch_and_item_id(self, branch_id, item_id):
        stmt = select(ItemStock).where(
            ItemStock.branch_id == branch_id,
            ItemStock.item_id == item_id
        )
        return self.db.execute(stmt).scalars().first()
    