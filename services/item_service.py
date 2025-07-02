from repository.item_repository import ItemRepository
from repository.price_repository import PriceRepository
from werkzeug.exceptions import BadRequest, InternalServerError

def get_item_by_id(db, item_id):
    item_repository = ItemRepository(db)
    item = item_repository.get_by_id(item_id)
    if not item:
        raise BadRequest("Item not found")
    return item

def get_all_items(db):
    item_repository = ItemRepository(db)
    items = item_repository.list_all()
    return items

def create_item(db, new_item):
    item_repository = ItemRepository(db)
    return item_repository.create(new_item)

def delete_item(db, item_id):
    item_repository = ItemRepository(db)
    item = item_repository.get_by_id(item_id)
    if not item:
        raise BadRequest("Item not found")
    item_repository.delete(item)

def update_item(db, item_id, updates):
    item_repository = ItemRepository(db)
    item = item_repository.get_by_id(item_id)
    if not item:
        raise BadRequest("Item not found")
    if not updates:
        raise BadRequest("No updates provided")
    return item_repository.update(item, updates)


def get_category_by_item_id(db, item_id):
    item_repository = ItemRepository(db)
    category = item_repository.get_category_by_item_id(item_id)
    if not category:
        raise BadRequest("Category not found for this item")
    return category

def get_item_stocks_by_item_id(db, item_id):
    item_repository = ItemRepository(db)
    item_stocks = item_repository.get_item_stocks_by_item_id(item_id)
    return item_stocks

def get_item_price_by_id_and_amount(db, item_id, amount):
    item_repository = ItemRepository(db)
    price = item_repository.get_item_price_by_id_and_amount(item_id, amount)
    if price is None:
        raise InternalServerError("Price not found for this item and amount")
    return price

def get_item_prices_by_id(db, item_id):
    price_repo = PriceRepository(db)
    prices = price_repo.get_prices_by_item_id(item_id)
    return prices
