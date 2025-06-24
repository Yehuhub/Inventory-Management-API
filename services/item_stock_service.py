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

def get_item_stock_by_id(db, item_stock_id):
    repo = ItemStockRepository(db)
    item_stock = repo.get_by_id(item_stock_id)
    if not item_stock:
        raise NotFound("Item stock not found")
    return item_stock

def get_all_items_stock(db):
    repo = ItemStockRepository(db)
    item_stocks = repo.list_all()
    if not item_stocks:
        raise NotFound("No stock found")
    return item_stocks

def create_item_stock(db, new_item_stock):
    repo = ItemStockRepository(db)
    return repo.create(new_item_stock)

def delete_item_stock(db, item_stock_id):
    repo = ItemStockRepository(db)
    item_stock = repo.get_by_id(item_stock_id)
    if not item_stock:
        raise NotFound("Item stock not found")
    repo.delete(item_stock)

def get_item_stock_by_branch_and_item(db, branch_id, item_stock_id):
    repo = ItemStockRepository(db)
    item_stock = repo.get_item_stock_by_branch_and_item_id(branch_id, item_stock_id)
    if not item_stock:
        raise NotFound("Stock not found for the item and branch")
    return item_stock