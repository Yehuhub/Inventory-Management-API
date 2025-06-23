from repository.item_stock_repository import ItemStockRepository
from werkzeug.exceptions import NotFound, BadRequest

def update_item_stock(db, item_stock_id, updates):
    repo = ItemStockRepository(db)
    item_stock = repo.get_by_id(item_stock_id)
    if not item_stock:
        raise NotFound("Item Stock not found")
    if not updates:
        raise BadRequest("No updates provided")
    return repo.update(item_stock, updates)

def get_item_by_id(db, item_id):
    repo = ItemStockRepository(db)
    item_stock = repo.get_by_id(item_id)
    if not item_stock:
        raise NotFound("Item not found")
    return item_stock

def get_all_items(db):
    repo = ItemStockRepository(db)
    item_stock = repo.list_all()
    if not item_stock:
        raise NotFound("No items found")
    return item_stock

def create_item(db, new_item):
    repo = ItemStockRepository(db)
    return repo.create(new_item)

def delete_item(db, item_id):
    repo = ItemStockRepository(db)
    item_stock = repo.get_by_id(item_id)
    if not item_stock:
        raise NotFound("Item not found")
    repo.delete(item_stock)
